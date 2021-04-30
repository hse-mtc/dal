module.exports = {
  root: true,
  env: {
    browser: true,
    es6: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:vue/recommended",
    "@vue/standard",
    "airbnb-base",
  ],
  globals: {
    Atomics: "readonly",
    SharedArrayBuffer: "readonly",
    window: true,
    document: true,
    location: true,
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: "module",
  },
  plugins: ["vue"],
  rules: {
    "no-console": "off",
    "no-unused-vars": 0,
    "import/no-cycle": 0,
    "import/prefer-default-export": 0,
    "import/no-extraneous-dependencies": 0,
    "arrow-parens": [2, "as-needed"],
    "key-spacing": [
      "warn",
      {
        singleLine: {
          beforeColon: false,
          afterColon: true,
        },
        multiLine: {
          beforeColon: false,
          afterColon: true,
        },
      },
    ],
    "quote-props": ["error", "as-needed"],
    quotes: ["error", "double"],
    "space-before-function-paren": [2, "never"],
    "vue/array-bracket-spacing": "error",
    "vue/arrow-spacing": "error",
    "vue/block-spacing": "error",
    "vue/brace-style": "error",
    "vue/camelcase": "error",
    "vue/comma-dangle": "error",
    "comma-dangle": ["error", "always-multiline"],
    "vue/component-name-in-template-casing": "error",
    "vue/eqeqeq": "error",
    "vue/key-spacing": "error",
    "vue/match-component-file-name": "error",
    "vue/object-curly-spacing": "error",
    "vue/max-attributes-per-line": [
      "error",
      {
        singleline: 3,
        multiline: {
          max: 1,
          allowFirstLine: false,
        },
      },
    ],
    "object-curly-spacing": ["error", "always"],
    "func-names": ["error", "as-needed"],
  },
};
