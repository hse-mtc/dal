module.exports = {
  presets: ["@vue/app"],
  plugins: [
    "@babel/plugin-proposal-optional-chaining",
    ["@babel/proposal-decorators", { legacy: true }],
    ["@babel/proposal-class-properties", { loose: true }],
  ],
};
