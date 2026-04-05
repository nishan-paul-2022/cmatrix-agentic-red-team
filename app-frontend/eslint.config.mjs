// eslint-config-next@16 ships a native ESLint flat config array — import directly.
// Do NOT use FlatCompat; it triggers @eslint/eslintrc's legacy validator which
// crashes with a circular-JSON error on eslint-plugin-react's plugin object.
import nextConfig from "eslint-config-next/core-web-vitals";
import prettier from "eslint-config-prettier";
import tseslint from "typescript-eslint";

const eslintConfig = [
  // Ignore generated/vendor output
  {
    ignores: [".next/**", "node_modules/**", "public/**"],
  },

  // Next.js flat config already includes: react, react-hooks, import,
  // jsx-a11y, @next/next, @typescript-eslint rules
  ...nextConfig,

  // Prettier must come last — disables all style rules that conflict
  prettier,

  // Project-specific rule overrides — re-declare @typescript-eslint plugin
  // so ESLint flat config can find it in the same config object
  {
    plugins: {
      "@typescript-eslint": tseslint.plugin,
    },
    rules: {
      "@typescript-eslint/no-unused-vars": [
        "warn",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
        },
      ],
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/explicit-module-boundary-types": "off",
      "react/react-in-jsx-scope": "off",
      "react/prop-types": "off",
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "prefer-const": "warn",
      "no-var": "error",
    },
  },
];

export default eslintConfig;
