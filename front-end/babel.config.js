module.exports = {
  presets: ["@vue/app"],
  plugins: [
    ["@babel/proposal-decorators", { legacy: true }],
    ["@babel/proposal-class-properties", { loose: true }],
  ],
};
