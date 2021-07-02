export default allow => {
  const meta = document.querySelector("meta[name=viewport]");
  const app = document.querySelector("#app");

  if (allow) {
    meta.content = "width=device-width, initial-scale=1";
    app.style.minWidth = "none";
  } else {
    meta.content = "width=1200, initial-scale=1";
    app.style.minWidth = "1200px";
  }
};
