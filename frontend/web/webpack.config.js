const { resolve } = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

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
            DEFAULT_HOST: process.env.DEFAULT_HOST,
            DEFAULT_PORT: process.env.DEFAULT_PORT,
        }),

        new MiniCssExtractPlugin({
            filename: "css/[name].min.css",
        }),

        new CopyWebpackPlugin({
            patterns: [{ from: "src/assets" }],
        }),
    ],
    devServer: {
        port: 8080,
        proxy: [
            {
                context: ["/api", "/docs", "/metrics"],
                target: process.env.API_URL,
            },
        ],
    },
    optimization: {
        minimize: true,
        minimizer: [
            new TerserPlugin({
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
