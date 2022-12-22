module.exports = {
  entry: {
    main: './src/index.js',
    // vendor: './src/vendor.js',
  },
  module: {
    rules: [
      {
        test: /\.(svg|png|jpe?g|gif)$/,
        type: 'asset/resource',
      },
      {
        test: /\.(html)$/,
        use: ['html-loader'],
      },
    ],
  },
};
