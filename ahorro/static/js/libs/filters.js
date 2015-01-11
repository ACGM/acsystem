(function () {

  angular.module('cooperativa.Ahorro.filters', [])
    .filter('posteo', function () {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('N', false)
                .replace('S', true);
        return input;
      };
    });
})();
