const path = require("path");
const CopyPlugin = require("copy-webpack-plugin");
const WasmPackPlugin = require("@wasm-tool/wasm-pack-plugin");

const dist = path.resolve(__dirname, "dist");

module.exports = {
  mode: "production",
  entry: {
    index: "./js/bootstrap.js"
  },
  experiments: {
      asyncWebAssembly: true
  },
  output: {
    path: dist,
    filename: "[name].js"
  },
  devServer: {
    static: dist,
  },
  plugins: [
    new CopyPlugin([
      path.resolve(__dirname, "static")
    ]),

    // Only the compiled index is needed at runtime. Copying all of ../full
    // would also ship the source dictionaries and the licence-restricted
    // words.hk/LIHKG inputs into dist/docs.
    new CopyPlugin([
      { from: path.resolve(__dirname, "../full/full.jyp_dict"), to: "full.jyp_dict" }
    ]),

    new WasmPackPlugin({
      crateDirectory: __dirname,
    }),
  ]
};
