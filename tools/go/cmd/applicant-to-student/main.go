package main

import (
	"bufio"
	"context"
	"crypto/tls"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/spf13/pflag"
	"resty.dev/v3"
)

var (
	baseURL        string
	email          string
	password       string
	applicantsFile string
	admissionYear  string
	milGroup       int
)

type TokenPair struct {
	Access  string `json:"access"`
	Refresh string `json:"refresh"`
}

var tokenPair TokenPair

func obtainToken(authClient *resty.Client) error {
	log.Println("Obtaining new token pair")
	_, err := authClient.R().
		SetBody(map[string]string{
			"email":    email,
			"password": password,
		}).
		SetResult(&tokenPair).
		Post("/api/auth/tokens/obtain/")
	return err
}

func refreshToken(authClient *resty.Client) error {
	log.Println("Refreshing access token")
	_, err := authClient.R().
		SetBody(map[string]string{
			"refresh": tokenPair.Refresh,
		}).
		SetResult(&tokenPair).
		Post("/api/auth/tokens/refresh/")
	return err
}

func main() {
	pflag.StringVar(&baseURL, "base-url", "https://dal.mtc.hse.ru", "Base URL for API requests")
	pflag.StringVar(&email, "email", "superuser@mail.com", "Admin email for authentication")
	pflag.StringVar(&password, "password", "qwerty", "Admin password for authentication")
	pflag.StringVar(&applicantsFile, "applicants-file", "applicants.txt", "File with applicants list (one FIO per line)")
	pflag.StringVar(&admissionYear, "admission-year", "2025", "Admission year")
	pflag.IntVar(&milGroup, "mil-group", 7, "Military group number (now use placeholder)")
	pflag.Parse()

	log.SetOutput(os.Stdout)

	ctx := context.Background()
	client := resty.New().SetBaseURL(baseURL).SetTLSClientConfig(&tls.Config{InsecureSkipVerify: true})
	authClient := resty.New().SetBaseURL(baseURL).SetTLSClientConfig(&tls.Config{InsecureSkipVerify: true})

	client.AddRequestMiddleware(func(c *resty.Client, r *resty.Request) error {
		if tokenPair.Access == "" {
			if err := obtainToken(authClient); err != nil {
				return err
			}
		}
		r.SetAuthToken(tokenPair.Access)
		return nil
	})

	client.AddResponseMiddleware(func(c *resty.Client, r *resty.Response) error {
		if r.StatusCode() == http.StatusUnauthorized {
			if err := refreshToken(authClient); err != nil {

				if err := obtainToken(authClient); err != nil {
					return err
				}
			}

			r.Request.SetAuthToken(tokenPair.Access)
			resp, err := r.Request.Execute(r.Request.Method, r.Request.URL)
			if err != nil {
				return err
			}
			*r = *resp
		}
		return nil
	})

	file, err := os.Open(applicantsFile)
	if err != nil {
		log.Fatalf("[FATAL] failed to open file: %v", err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		fio := strings.TrimSpace(scanner.Text())
		if fio == "" {
			continue
		}

		log.Printf("[INFO] Processing applicant: %s\n", fio)

		var searchResponse []struct {
			ID       int    `json:"id"`
			Fullname string `json:"fullname"`
		}

		resp, err := client.R().WithContext(ctx).
			SetQueryParam("mtc_admission_year", admissionYear).
			SetQueryParam("search", fio).
			SetResult(&searchResponse).
			SetBody(map[string]string{"applicant": fio}).
			Get("/api/ams/applicants/applications/")
		if err != nil {
			log.Printf("[ERROR] search for %s: %v\n", fio, err)
			continue
		}

		if len(searchResponse) == 0 {
			log.Printf("[ERROR] no results for %s\n", fio)
			continue
		}

		if len(searchResponse) > 1 {
			log.Printf("[ERROR] multiple results for %s: %+v\n", fio, searchResponse)
			continue
		}

		userID := searchResponse[0].ID

		var applicantResponse map[string]any

		resp, err = client.R().WithContext(ctx).
			SetResult(&applicantResponse).
			Get(fmt.Sprintf("api/ams/applicants/%d/", userID))
		if err != nil {
			log.Printf("[ERROR] get applicant %s (ID %d): %v\n", fio, userID, err)
			continue
		}

		// move data to register_from_applicant format
		universityInfo := applicantResponse["university_info"].(map[string]any)
		universityInfo["program"] = universityInfo["program"].(map[string]any)["id"]
		delete(applicantResponse, "photo")
		delete(applicantResponse, "family")
		applicantResponse["milgroup"] = milGroup

		resp, err = client.R().WithContext(ctx).
			SetHeader("Content-Type", "application/json").
			SetBody(applicantResponse).
			Post("api/lms/students/register_from_applicant/")
		if err != nil {
			log.Printf("[ERROR] register student from applicant %s (ID %d): %v\n", fio, userID, err)
			continue
		}

		if resp.StatusCode() != http.StatusOK {
			log.Printf("[ERROR] register student from applicant %s with resp %s (ID %d): unexpected status code %v\n", fio, resp.String(), userID, resp.StatusCode())
			continue
		}

		log.Printf("[SUCCESS] registered student from applicant %s (ID %d)\n", fio, userID)
	}
	if err := scanner.Err(); err != nil {
		log.Fatalf("[FATAL] failed to read file: %v", err)
	}
}
