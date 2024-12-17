
//const {defaults} = require("jest-config")

module.exports = {
   verbose: true,
   roots: ["<rootDir>/tests/","<rootDir>/src/"],
   moduleFileExtensions: ["js","vue"],
   moduleNameMapper: {
      "^@/(.*)$": "<rootDir>/src/$1",
      "\\.(css|sass)$":"<rootDir>/src/stylestub.js",
   },
   transform: {
      "^.+\\.js$": "babel-jest",
      "^.+\\.vue$": "vue-jest",
      ".+\\.(gif|png|jpg|svg|ttf|woff|woff2)$": "jest-transform-stub"
   },
   "transformIgnorePatterns":[
       "node_modules/?!(vue-100vh)"
   ]
}
