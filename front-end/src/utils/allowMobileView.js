export default (allow) => {
  const meta = document.querySelector("meta[name=viewport]");
  const app = document.querySelector("#app");

  if (allow) {
    meta.content = "width=device-width, initial-scale=1";
    app.style = "min-width: none";
  } else {
    meta.content = "width=1200, initial-scale=1";
    app.style = "min-width: 1200px";
  }
};
