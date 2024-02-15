const DEVELOPMENT = process.env.NODE_ENV === "development";
const PRODUCTION = process.env.NODE_ENV === "production";
const mode = DEVELOPMENT ? "development" : "production";

module.exports = {
  entry: {
    client: './src/client.js'
  },
  output: {
    filename: '[name].js',
    path: `${__dirname}/public`
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      }
    ]
  },
  mode: mode,
  resolve: {
    extensions: ['.js', '.jsx'],
    modules: ['node_modules']
  },
}