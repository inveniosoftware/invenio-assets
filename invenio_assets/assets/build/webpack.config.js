/*
 * This file is part of Invenio.
 * Copyright (C) 2017-2018 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

const CleanWebpackPlugin = require('clean-webpack-plugin');
const config = require('./config');
const ManifestPlugin = require('webpack-manifest-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const safePostCssParser = require('postcss-safe-parser');
const TerserPlugin = require('terser-webpack-plugin');
const webpack = require('webpack');

var webpackConfig = {
  entry: config.entry,
  context: config.build.context,
  resolve: {
    extensions: ['*', '.js']
  },
  output: {
    path: config.build.assetsPath,
    filename: 'js/[name].[chunkhash].js',
    chunkFilename: 'js/[id].[chunkhash].js',
    publicPath: config.build.assetsURL
  },
  optimization: {
    minimizer: [
      new TerserPlugin({
        parallel: true,
        cache: true
      }),
      new OptimizeCSSAssetsPlugin({
        cssProcessorOptions: {
          parser: safePostCssParser,
          map: false
        }
      })
    ],
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: "vendor",
          chunks: "initial",
        },
      },
      chunks: 'all',
    },
    // Extract webpack runtime and module manifest to its own file in order to
    // prevent vendor hash from being updated whenever app bundle is updated.
    runtimeChunk: {
      name: 'manifest'
    }
  },
  module: {
    rules: [
      {
          test: require.resolve('jquery'),
          use: [{
              loader: 'expose-loader',
              options: 'jQuery'
          },{
              loader: 'expose-loader',
              options: '$'
          }]
      },
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: [
          {
            loader: 'babel-loader',
          }
        ],
      },
      {
        test: /\.(js|jsx)$/,
        enforce: "pre",
        exclude: /node_modules/,
        use: [
          {
            options: {
              formatter: require('eslint-friendly-formatter'),
              eslintPath: require.resolve('eslint'),
            },
            loader: require.resolve('eslint-loader'),
          }
        ]
      },
      {
        test: /\.(scss|css)$/,
        use: [
          MiniCssExtractPlugin.loader,
            {
                loader: "css-loader",
                options: {
                    minimize: {
                        safe: true
                    }
                }
            },
            {
                loader: "sass-loader",
                options: {}
            }
        ]
      },
      // Inline images smaller than 10k
      {
        test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
        use: [
          {
            loader: require.resolve('url-loader'),
            options: {
              limit: 10000,
              name: 'img/[name].[hash:7].[ext]'
            }
          }
        ],
      },
      // Inline webfonts smaller than 10k
      {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        use: [
          {
            loader: require.resolve('file-loader'),
            options: {
              limit: 10000,
              name: 'fonts/[name].[hash:7].[ext]'
            }
          }
        ],
      }
    ]
  },
  // devtool: process.env.NODE_ENV === 'production' ? 'source-map' : 'cheap-source-map',
  plugins: [
    // Pragmas
    new webpack.DefinePlugin({
      'process.env': process.env.NODE_ENV
    }),
    new MiniCssExtractPlugin({
      // Options similar to the same options in webpackOptions.output
      // both options are optional
      filename: "css/[name].[contenthash].css",
      chunkFilename: "css/[name].[contenthash].css",
    }),
    // Removes the dist folder before each run.
    new CleanWebpackPlugin(config.build.assetsPath, {allowExternal: true}),
    // Automatically inject jquery
    new webpack.ProvidePlugin({
        jQuery: 'jquery/src/jquery',
        $: 'jquery/src/jquery',
        jquery: 'jquery/src/jquery',
        'window.jQuery': 'jquery/src/jquery'
    }),
    // Write manifest file which Python will read.
    new ManifestPlugin({
      fileName: 'manifest.json',
      stripSrc: true,
      publicPath: config.build.assetsURL
    })
  ]
}

if (process.env.npm_config_report) {
  var BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin
  webpackConfig.plugins.push(new BundleAnalyzerPlugin())
}

module.exports = webpackConfig
