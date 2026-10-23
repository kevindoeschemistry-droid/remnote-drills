// Multi-widget RemNote plugin build (same layout as remnoteio/remnote-plugin-template-react).
// Every file in src/widgets/ becomes  dist/<name>.js  (native) and  dist/<name>-sandbox.js.
// index.html is generated, so public/index.html is no longer needed.
const path = require("path");
const glob = require("glob");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyPlugin = require("copy-webpack-plugin");
const { ProvidePlugin, BannerPlugin } = require("webpack");

const isProd = process.env.NODE_ENV === "production";
const SANDBOX_SUFFIX = "-sandbox";

const entry = glob.sync("./src/widgets/**/*.tsx").reduce((obj, file) => {
  const name = path
    .relative("src/widgets", file)
    .replace(/\.[tj]sx?$/, "")
    .replace(/\\/g, "/");
  obj[name] = file;
  obj[`${name}${SANDBOX_SUFFIX}`] = file;
  return obj;
}, {});

module.exports = {
  mode: isProd ? "production" : "development",
  devtool: isProd ? false : "cheap-module-source-map",
  entry,
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "[name].js",
    publicPath: "",
    clean: true,
  },
  resolve: { extensions: [".tsx", ".ts", ".js"] },
  module: {
    rules: [
      {
        test: /\.[jt]sx?$/,
        loader: "esbuild-loader",
        options: { loader: "tsx", target: "es2020" },
      },
      {
        // styles are injected at runtime so every widget carries its own CSS
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      // KaTeX fonts: inline woff2 (what every current browser uses), skip the rest
      { test: /\.woff2$/, type: "asset/inline" },
      { test: /\.(woff|ttf)$/, type: "asset/resource", generator: { emit: false } },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      templateContent: `
      <body></body>
      <script type="text/javascript">
      const params = Object.fromEntries(new URLSearchParams(window.location.search).entries());
      const widgetName = params["widgetName"];
      if (widgetName == undefined) { document.body.innerHTML += "Widget ID not specified."; }
      const s = document.createElement("script");
      s.type = "module";
      s.src = widgetName + "${SANDBOX_SUFFIX}.js";
      document.body.appendChild(s);
      </script>`,
      filename: "index.html",
      inject: false,
    }),
    new ProvidePlugin({ React: "react", reactDOM: "react-dom" }),
    new BannerPlugin({
      banner: (file) => (!file.chunk.name.includes(SANDBOX_SUFFIX) ? "const IMPORT_META=import.meta;" : ""),
      raw: true,
    }),
    new CopyPlugin({
      patterns: [
        { from: "public", to: ".", globOptions: { ignore: ["**/index.html"] }, noErrorOnMissing: true },
        { from: "README.md", to: "." }, // RemNote's zip upload requires a README
      ],
    }),
  ],
  devServer: {
    port: 3005,
    hot: false,
    liveReload: true,
    static: { directory: path.join(__dirname, "public") },
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "baggage, sentry-trace",
    },
  },
  performance: { hints: false },
};
