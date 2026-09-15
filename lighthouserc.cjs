const baseUrl = process.env.LHCI_URL ?? "http://127.0.0.1:3000";
const chromePath = process.env.CHROME_PATH;

module.exports = {
  ci: {
    collect: {
      url: [`${baseUrl}/tasks`, `${baseUrl}/calendar`, `${baseUrl}/grimo`],
      numberOfRuns: 1,
      settings: {
        formFactor: "mobile",
        screenEmulation: {
          mobile: true,
          width: 412,
          height: 915,
          deviceScaleFactor: 2,
        },
        ...(chromePath ? { chromePath } : {}),
      },
    },
    assert: {
      assertions: {
        "categories:accessibility": ["error", { minScore: 0.9 }],
        "categories:best-practices": ["warn", { minScore: 0.8 }],
        "categories:performance": "warn",
        "categories:pwa": "warn",
      },
    },
    upload: {
      target: "filesystem",
      outputDir: "output/lighthouse",
    },
  },
};
