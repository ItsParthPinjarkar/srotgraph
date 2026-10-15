import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import nextPlugin from "@next/eslint-plugin-next";

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ["**/*.ts", "**/*.tsx"],
    extends: [nextPlugin.configs.recommended],
    rules: {
      "@typescript-eslint/no-unused-vars": "warn",
      "@next/next/no-img-element": "off",
    },
  },
  {
    ignores: ["**/*.js", "**/*.json", "next-env.d.ts"],
  }
);
