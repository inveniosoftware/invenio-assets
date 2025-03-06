/*
 * This file is part of Invenio.
 * Copyright (C) 2017-2018 CERN.
 * Copyright (C) 2022-2023 Graz University of Technology.
 * Copyright (C) 2023-2025 TU Wien.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */
// https://birtles.blog/2024/08/14/lessons-learned-switching-to-rspack/

const BundleTracker = require("webpack-bundle-tracker");
const config = require("./config");
const path = require("path");

// Use rspack
const rspack = require("@rspack/core");

// Load aliases from config and resolve their full path
let aliases = {};
if (config.aliases) {
  aliases = Object.fromEntries(
    Object.entries(config.aliases).map(([alias, alias_path]) => [
      alias,
      path.resolve(config.build.context, alias_path),
    ]),
  );
}

// Create copy patterns from config
let copyPatterns = [];
if (config.copy) {
  for (copy of config.copy) {
    const copyPattern = {
      from: path.resolve(__dirname, copy.from),
      to: path.resolve(__dirname, copy.to),
    };

    copyPatterns.push(copyPattern);
  }
}

const prod = process.env.NODE_ENV === "production";

var webpackConfig = {
  mode: process.env.NODE_ENV,
  entry: config.entry,
  context: config.build.context,
  stats: {
    //preset: 'verbose',
    warnings: true,
    errors: true,
    errorsCount: true,
    errorStack: true,
    errorDetails: true,
    children: true,
  },
  resolve: {
    extensions: ["*", ".js", ".jsx"],
    symlinks: false,
    alias: aliases,
    fallback: {
      zlib: require.resolve("browserify-zlib"),
      stream: require.resolve("stream-browserify"),
      https: require.resolve("https-browserify"),
      http: require.resolve("stream-http"),
      url: false,
      assert: false,
    },
  },
  output: {
    clean: true, // replaces CleanWebpackPlugin
    path: config.build.assetsPath,
    filename: "js/[name].[chunkhash].js",
    chunkFilename: "js/[id].[chunkhash].js",
    publicPath: config.build.assetsURL,
  },
  optimization: {
    minimizer: [
      new rspack.SwcJsMinimizerRspackPlugin({
        compress: {
          ecma: 5,
          // warnings: false,
          // Disabled because of an issue with Uglify breaking seemingly valid code:
          // https://github.com/facebook/create-react-app/issues/2376
          // Pending further investigation:
          // https://github.com/mishoo/UglifyJS2/issues/2011
          comparisons: false,
          // Disabled because of an issue with Terser breaking valid code:
          // https://github.com/facebook/create-react-app/issues/5250
          // Pending further investigation:
          // https://github.com/terser-js/terser/issues/120
          inline: 2,
        },
        mangle: {
          safari10: true,
        },
      }),

      // would be nice, but not workable at the moment, no idea why
      new rspack.LightningCssMinimizerRspackPlugin({
        minimizerOptions: {
          targets: [
            "last 2 Chrome versions",
            "Firefox ESR",
            "last 2 Safari versions",
          ],
        },
      }),
    ],
    splitChunks: {
      chunks: "all",
    },
    // Extract webpack runtime and module manifest to its own file in order to
    // prevent vendor hash from being updated whenever app bundle is updated.
    runtimeChunk: {
      name: "manifest",
    },
  },
  module: {
    rules: [
      {
        test: require.resolve("jquery"),
        use: [
          {
            loader: "expose-loader",
            options: {
              exposes: ["$", "jQuery"],
            },
          },
        ],
      },
      {
        test: /\.(js|jsx)$/,
        exclude: [/node_modules/, /@babel(?:\/|\\{1,2})runtime/],
        loader: "builtin:swc-loader",
        options: {
          jsc: {
            parser: {
              syntax: "ecmascript",
              jsx: true,
            },
            externalHelpers: true,
            transform: {
              react: {
                development: !prod,
                useBuiltins: true,
              },
            },
          },
          env: {
            targets: "Chrome >= 48",
          },
        },
      },

      {
        test: /\.(scss|css)$/,
        use: [
          rspack.CssExtractRspackPlugin.loader,
          "css-loader",
          "sass-loader",
        ],
      },
      {
        test: /\.(less)$/,
        use: [
          rspack.CssExtractRspackPlugin.loader,
          "css-loader",
          "less-loader",
        ],
      },

      // Rspack
      // Inline images smaller than 10k
      {
        test: /\.(avif|webp|png|jpe?g|gif|svg)(\?.*)?$/,
        type: "asset/resource",
      },
      // no mimetype for ".cur" in mimetype database, specify it with `generator`
      {
        test: /\.(cur)(\?.*)?$/,
        type: "asset/inline",
        generator: {
          dataUrl: {
            encoding: "base64",
            mimetype: "image/x-icon",
          },
        },
      },
      // Inline webfonts smaller than 10k
      {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        type: "asset/resource",
        generator: {
          filename: "fonts/[name].[contenthash:7].[ext]",
        },
      },
    ],
  },
  devtool:
    process.env.NODE_ENV === "production" ? "source-map" : "inline-source-map",
  plugins: [
    new rspack.DefinePlugin({
      "process.env": process.env.NODE_ENV,
    }),
    new rspack.CssExtractRspackPlugin({
      // Options similar to the same options in webpackOptions.output
      // both options are optional
      filename: "css/[name].[contenthash].css",
      chunkFilename: "css/[name].[contenthash].css",
    }),

    // Copying relevant CSS files as TinyMCE tries to import css files from the dist/js folder of static files
    new rspack.CopyRspackPlugin({
      patterns: copyPatterns,
    }),
    // Automatically inject jquery
    new rspack.ProvidePlugin({
      jQuery: "jquery",
      $: "jquery",
      jquery: "jquery",
      "window.jQuery": "jquery",
    }),
    // Write manifest file which Python will read.
    new BundleTracker({
      path: config.build.assetsPath,
      filename: path.join(config.build.assetsPath, "manifest.json"),
      publicPath: config.build.assetsURL,
    }),
  ],
  performance: { hints: false },
  watchOptions: {
    followSymlinks: true,
    ignored: '**/.git', // The default would also ignore "node_modules" which we don't want
  },
  experiments: {
    css: false,
  },
  devServer: {
    hot: true, // Enable Hot Module Replacement (HMR)
    liveReload: true, // Enable live reload
  },
};

if (process.env.npm_config_report) {
  var BundleAnalyzerPlugin =
    require("webpack-bundle-analyzer").BundleAnalyzerPlugin;
  webpackConfig.plugins.push(new BundleAnalyzerPlugin());
}

module.exports = webpackConfig;
