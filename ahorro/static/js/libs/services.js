(function () {

  angular.module('cooperativa.Ahorro.services', [])

    .factory('AhorroService', ['$http', '$q', '$filter', '$window', function ($http, $q, $filter, $window) {
      var posteo = $filter('posteo');
      var localStorage = $window.localStorage;
      var ahorrado={
        id : null,
        socio : "1",
        balance : "30000.00",
        disponible : "15000.00",
        maestra : [{
          id: null,
          fecha : Date(),
          monto : '15000.00',
          interes : '0.25',
          balance : '30000.00',
          estatus : false,
          cuentas : [
          {
            id : null,
            fecha : Date,
            cuenta : 11,
            referencia : "",
            auxiliar : null,
            tipoDoc : '1',
            estatus : 'p',
            debito : '15000.00',
            credito : '0'
          },
          {
            id : null,
            fecha : Date.now(),
            cuenta : 22,
            referencia : "",
            auxiliar : null,
            tipoDoc : '1',
            estatus : 'p',
            debito : '0',
            credito : '15000.00'
          }]

        }]
      };


      function allAhorro() {
        var deferred = $q.defer();

        $http.get('/ahorrojson?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      function ahorroBySocio(socio) {
        socio = t(socio);
        var deferred = $q.defer();

        all().then(function (data) {
          var results = data.filter(function (ahorro) {
            return ahorro.socio === socio;
          });

          if (results.length > 0) {
            deferred.resolve(results[0]);
          } else {
            deferred.reject();
          }

        });

        return deferred.promise;
      }

      function saveAhorro(ahorro) {
        var deferred =$q.defer();
        $http.post('http://localhost:8000/ahorrojson?format=json',JSON.stringify({'ahorro':ahorrado})
          .success(function (data){
            deferred.resolve(data);
          }).error(function(data){
            deferred.resolve(data);
          })
        );
        return deferred.promises;   
        
      }

      return {
        allAhorro: allAhorro,
        ahorroBySocio: ahorroBySocio,
        saveAhorro: saveAhorro
      };

    }]);

})();