const { resolve } = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
    entry: {
        index: ["./src/js/index.js", "./src/css/index.css"],
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, "css-loader"],
            },
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: "src/index.html",
            minify: {
                collapseWhitespace: true,
            },
            DEFAULT_PORT: process.env.DEFAULT_PORT,
            GOOGLE_ANALYTICS: process.env.GOOGLE_ANALYTICS,
            ADSENSE_VERIFICATION: process.env.ADSENSE_VERIFICATION,
        }),

        new MiniCssExtractPlugin({
            filename: "css/[name].min.css",
        }),
    ],
    devServer: {
        port: 8080,
        proxy: {
            "/api/": {
                target: "http://api:8000",
            },
        },
    },
    optimization: {
        minimize: true,
        minimizer: [
            new UglifyJsPlugin({
                include: /\.js$/,
            }),
            new CssMinimizerPlugin(),
        ],
    },
    output: {
        path: resolve(__dirname, "dist"),
        filename: "js/[name].min.js",
    },
};
