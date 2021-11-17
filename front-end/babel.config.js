module.exports = {
  presets: ["@vue/cli-plugin-babel/preset"],
  plugins: [
    "@babel/plugin-proposal-optional-chaining",
    ["@babel/proposal-decorators", { legacy: true }],
    ["@babel/proposal-class-properties", { loose: true }],
  ],
};
