(function (_) {

  angular.module('cooperativa.desembolsoelectronico', ['ngAnimate'])

    .factory('DesembolsoElectronicoService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      
      //Llenar el listado de prestamos
      function listadoPrestamos() {
        var deferred = $q.defer();

        $http.get('/prestamosDesembolsoElectronicojson/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un numero de prestamo en especifico en listado de prestamos
      function byNoPrestamo(NoPrestamo) {
        var deferred = $q.defer();
        listadoPrestamos().then(function (data) {
          var result = data.filter(function (documento) {
            return documento.noPrestamo == NoPrestamo;
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }


      //Buscar Prestamos por socio
      function PrestamosbySocio(codigoSocio){
        var deferred = $q.defer();

        listadoPrestamos().then(function (data) {
          var results = data.filter(function (registros) {
            return registros.socioCodigo == codigoSocio;
          });

          if(results.length > 0) {
            deferred.resolve(results);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }

      return {
        listadoPrestamos: listadoPrestamos,
        byNoPrestamo: byNoPrestamo,
        PrestamosbySocio: PrestamosbySocio
        // PrestamoById: PrestamoById
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('DesembolsoPrestamosCtrl', ['$scope', '$filter', '$timeout', '$window', 'DesembolsoElectronicoService', 'MaestraPrestamoService',
                                        function ($scope, $filter, $timeout, $window, DesembolsoElectronicoService, MaestraPrestamoService) {
      
      //Inicializacion de variables
      $scope.disabledButton = 'Boton-disabled';
      $scope.disabledButtonBool = true;
      $scope.posteof = '*';
      $scope.errorShow = false;
      $scope.showLP = true;
      $scope.regAll = false;

      $scope.prestamosSeleccionados = [];
      $scope.reg = [];
      $scope.valoresChk = [];
      $scope.dataH = {};
      $scope.prestamo = {};

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLP = 'UpArrow';

      
      // Mostrar/Ocultar panel de Listado de Facturas
      $scope.toggleLP = function() {
        $scope.showLP = !$scope.showLP;

        if($scope.showLP === true) {
          $scope.ArrowLP = 'UpArrow';
        } else {
          $scope.ArrowLP = 'DownArrow';
        }
      }


      //Listado de todos los prestamos
      $scope.listadoPrestamos = function() {
        $scope.NoFoundDoc = '';
        $scope.prestamosSeleccionados = [];
        $scope.valoresChk = [];

        DesembolsoElectronicoService.listadoPrestamos().then(function (data) {
          $scope.prestamos = data;
          $scope.regAll = false;

          if(data.length > 0) {
            $scope.verTodos = 'ver-todos-ei';

            var i = 0;
            data.forEach(function (data) {
              $scope.valoresChk[i] = false;
              i++;
            });
          }
        });
      }

      //Buscar un prestamo en especifico
      $scope.filtrarPorNoPrestamo = function(NoPrestamo) {
        try {
          DesembolsoElectronicoService.byNoPrestamo(NoPrestamo).then(function (data) {
            $scope.prestamos = data;

            if(data.length > 0) {
              $scope.verTodos = '';
              $scope.NoFoundDoc = '';
            }
          }, 
            (function () {
              $scope.NoFoundDoc = 'No se encontró el prestamo #' + NoPrestamo;
            }
          ));          
        } catch (e) {
          console.log(e);
        }
      }

      //Buscar Documento por ENTER
      $scope.buscarPrestamo = function($event, NoPrestamo) {
        if($event.keyCode == 13) {
          $scope.filtrarPorNoPrestamo(NoPrestamo);
        }
      }

      //Buscar prestamos en especifico por socio
      $scope.filtrarPorSocio = function(codigoSocio) {
        try {
          DesembolsoElectronicoService.PrestamosbySocio(codigoSocio).then(function (data) {
            $scope.prestamos = data;

            if(data.length > 0) {
              $scope.verTodos = '';
              $scope.NoFoundDoc = '';
            }
          }, 
            (function () {
              $scope.NoFoundDoc = 'No se encontró prestamo para el socio: ' + codigoSocio;
            }
          ));          
        } catch (e) {
          console.log(e);
        }
      }

      //Buscar Documento por ENTER (by Socio)
      $scope.buscarPrestamoBySocio = function($event, codigoSocio) {
        if($event.keyCode == 13) {
          $scope.filtrarPorSocio(codigoSocio);
        }
      }

      //Marcar Prestamo como Cheque
      $scope.marcarPrestamoDC = function($event, accion) {
        $event.preventDefault();

        MaestraPrestamoService.MarcarPrestamoDC($scope.prestamosSeleccionados, accion).then(function (data) {
          if(data == 1) {
            $scope.listadoPrestamos();
          } else {
            $scope.mostrarError(data);
          }
        }, function() {
          $scope.mostrarError("Hubo un error interno en la aplicacion, contacte al administrador.");
        })
      }

      //Cuando se le de click al checkbox del header.
      $scope.seleccionAll = function() {

        $scope.prestamos.forEach(function (data) {
          if ($scope.regAll === true){

            $scope.valoresChk[data.noPrestamo] = true;
            $scope.prestamosSeleccionados.push(data);
          }
          else{

            $scope.valoresChk[data.noPrestamo] = false;
            $scope.prestamosSeleccionados.splice(data);
          }
        });
      }

      //Cuando se le de click a un checkbox de la lista
      $scope.selectedReg = function(iReg) {
        index = $scope.prestamos.indexOf(iReg);

        if ($scope.reg[$scope.prestamos[index].noPrestamo] === true){
          $scope.prestamosSeleccionados.push($scope.prestamos[index]);
        }
        else{
          $scope.prestamosSeleccionados = _.without($scope.prestamosSeleccionados, _.findWhere($scope.prestamosSeleccionados, {noPrestamo : iReg.noPrestamo}));
        }
      }

      //Imprimir Recibido Conforme
      $scope.imprimirRC = function(prestamo) {
      $window.sessionStorage['prestamoRC'] = JSON.stringify(prestamo);
        $window.open('/prestamos/print/recibidoconforme/', target='_blank'); 
      }
     

    }])

  //****************************************************
  //CONTROLLERS PRINT DOCUMENT                         *
  //****************************************************
  .controller('ImprimirDesembolsoElectronicoCtrl', ['$scope', '$filter', '$window', 'DesembolsoElectronicoService', 
                                          function ($scope, $filter, $window, DesembolsoElectronicoService) {
    // $scope.factura = JSON.parse($window.sessionStorage['des']);
    $scope.dataH = {};
    $scope.dataD = [];

    



  }]);
   

})(_);