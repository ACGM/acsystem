(function (_) {

  angular.module('cooperativa.nomina', ['ngAnimate'])
    
    .factory('NominaService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      // Retornar las nominas generadas
      function nominasGeneradas() {
        var deferred = $q.defer();

        $http.get('/api/nominasgeneradas/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

          return deferred.promise;
      }

      // Retornar detalle de nomina generada
      function detalleNomina(fecha) {
        var deferred = $q.defer();
        if(fecha != undefined) {
          url = '/api/nomina/detalle/fecha/?format=json'.replace('fecha',fecha);
        } else {
          url = '/api/nomina/detalle/?format=json';
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

          return deferred.promise;
      }

      function detalleEmpleado(nomina,empleado) {
        var deferred = $q.defer();
        detalleNomina(nomina).then(function (data) {
          var result = data.filter(function (emp) {
            return emp.id == empleado.id;
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });

        return deferred.promise;
      }

      // Retornar los tipos de nominas
      function tiposNominas() {
        var deferred = $q.defer();

        $http.get('/api/tiposnomina/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

          return deferred.promise;
      }


      //Generar nomina (parametros: Fecha y Tipo de Nomina [y Nota])
      function generaNomina(fecha, tipo, quincena, nota) {
        var deferred = $q.defer();

        $http.post('/nomina/generar/', JSON.stringify({'fechaNomina': fecha, 'tipoNomina': tipo, 'quincena': quincena, 'nota': nota})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;

      }

      return {
        nominasGeneradas: nominasGeneradas,
        generaNomina: generaNomina,
        tiposNominas: tiposNominas,
        detalleNomina: detalleNomina,
        detalleEmpleado: detalleEmpleado
      };

    }])

    //****************************************************
    //CONTROLLERS                                        *
    // GENERAR NOMINA                                    *
    //****************************************************
    .controller('GeneraNominaCtrl', ['$scope', '$rootScope', 'NominaService', function ($scope, $rootScope, NominaService) {
      $scope.showGN = true;
      $scope.nominaH = {};

      // Mostrar/Ocultar panel de Generar Nomina
      $scope.toggleGN = function() {
        $scope.showGN = !$scope.showGN;
      }

      //Generar la nomina
      $scope.generarNomina = function() {
        try {
          if ($scope.FormGeneraNomina.$valid) {
            var fecha = $scope.nominaH.fechaNomina.split('/');
            var fechaFormatted = fecha[2] + '-' + fecha[1] + '-' + fecha[0];

            var tipo = $scope.nominaH.tipoNomina;
            var nota = $scope.nominaH.nota != undefined? $scope.nominaH.nota : '';
            var quincena;

            if(parseInt(fecha[0]) > 15) {
              quincena = 2;
            } else {
              quincena = 1;
            }

            NominaService.generaNomina(fechaFormatted,tipo,quincena,nota).then(function (data) {
              console.log(data);
              $rootScope.getNominasGeneradas();
            });
          } else {
            throw "Verifique que ha completado toda la información requerida.";

          }

        } catch (e) {
          console.log(e);
        }
      }

      // Todos los tipos de Nominas
      $scope.tiposNominas = function() {
        NominaService.tiposNominas().then(function (data) {
          $scope.tiposN = data;
        });
      }

    }])


    //****************************************************
    //CONTROLLERS                                        *
    // CONSULTA NOMINA                                   *
    //****************************************************
    .controller('ConsultarNominaCtrl', ['$scope', '$rootScope', 'NominaService', function ($scope, $rootScope, NominaService) {
      $scope.showCN = true;

      // Mostrar/Ocultar panel de Consultar Nomina
      $scope.toggleCN = function() {
        $scope.showCN = !$scope.showCN;
      }


      // Todas las nominas generadas
      $rootScope.getNominasGeneradas = function() {
        NominaService.nominasGeneradas().then(function (data) {
          $scope.nominas = data;
        });
      }


    }])


    //****************************************************
    //CONTROLLERS                                        *
    // DETALLE NOMINA                                    *
    //****************************************************
    .controller('DetalleNominaCtrl', ['$scope', '$rootScope', '$filter','NominaService', function ($scope, $rootScope, $filter, NominaService) {
      $scope.reg = [];
      $scope.empleado = [];

      // Retorna el detalle de una nomina
      $rootScope.getDetalleNomina = function(nomina) {
        $rootScope.nomina = nomina;

        NominaService.detalleNomina(nomina).then(function (data) {
          $scope.detalle = data;

          data.forEach(function (data) {
            $scope.reg[data.id] = '';
          });

        });
      }

      // Seleccionar un empleado para ver detalle
      $scope.selEmpleado = function(nomina, empleado) {

        $scope.reg.forEach(function (data, index) {
          $scope.reg[index] = '';
        });
        $scope.reg[empleado.id] = 'empleado-sel';

        NominaService.detalleEmpleado(nomina, empleado).then(function (data) {
          $scope.empleado.salario = $filter('number')(data[0].salario,2);
          $scope.empleado.ars = $filter('number')(data[0].ars,2);
          $scope.empleado.vacaciones = $filter('number')(data[0].vacaciones,2);
          $scope.empleado.afp = $filter('number')(data[0].afp,2);
          $scope.empleado.otrosIngresos = $filter('number')(data[0].otrosIngresos,2);
          $scope.empleado.isr = $filter('number')(data[0].isr,2);
          $scope.empleado.descPrestamos = $filter('number')(data[0].descPrestamos,2);
          $scope.empleado.descAhorros = $filter('number')(data[0].descAhorros,2);

        });
      }

    }])

})(_);