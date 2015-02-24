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
            return registros.codigoSocio == codigoSocio;
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
        listadoPrestamos: listadoPrestamos
        // byNoPrestamo: byNoPrestamo,
        // PrestamosbySocio: PrestamosbySocio,
        // PrestamoById: PrestamoById
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('DesembolsoPrestamosCtrl', ['$scope', '$filter', '$timeout', '$window', 'DesembolsoElectronicoService', 
                                        function ($scope, $filter, $timeout, $window, DesembolsoElectronicoService) {
      
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
          MaestraPrestamoService.byNoPrestamo(NoPrestamo).then(function (data) {
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
          MaestraPrestamoService.PrestamosbySocio(codigoSocio).then(function (data) {
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


      // Visualizar Prestamo (desglose)
      $scope.PrestamoFullById = function($event, prestamo) {
        $event.preventDefault();

        try {
          MaestraPrestamoService.PrestamoById(prestamo).then(function (data) {
            if(data.length > 0) {
              $scope.errorMsg = '';
              $scope.errorShow = false;

              //completar los campos
              // $scope.nuevaEntrada();

              var solicitudNo = data[0]['noSolicitudPrestamo'] == ''? data[0]['noSolicitudOD'] : data[0]['noSolicitudPrestamo'];

              $scope.dataH.noPrestamo = $filter('numberFixedLen')(data[0]['noPrestamo'],9);
              $scope.dataH.factura = data[0]['factura'];
              $scope.dataH.categoriaPrestamoDescrp = data[0]['categoriaPrestamoDescrp'];
              $scope.dataH.representanteCod = data[0]['representanteCodigo'];
              $scope.dataH.representanteDescrp = data[0]['representanteNombre'];
              $scope.dataH.socioCodigo = data[0]['socioCodigo'];
              $scope.dataH.socioNombre = data[0]['socioNombre'];
              $scope.dataH.socioCedula = data[0]['socioCedula'];
              $scope.dataH.pagarPor = ''; //data[0]['oficial'];
              $scope.dataH.oficial = data[0]['oficial'];
              $scope.dataH.localidad = data[0]['localidad'];
              $scope.dataH.estatus = data[0]['estatus'];
              $scope.dataH.posteadoFecha = data[0]['posteadoFecha'];

              $scope.prestamo.noSolicitud = $filter('numberFixedLen')(solicitudNo, 8);
              $scope.prestamo.monto = $filter('number')(data[0]['montoInicial'], 2);
              $scope.prestamo.tasaInteresAnual = data[0]['tasaInteresAnual'];
              $scope.prestamo.tasaInteresMensual = data[0]['tasaInteresMensual'];
              $scope.prestamo.pagoPrestamoAnterior = data[0]['pagoPrestamoAnterior'];
              $scope.prestamo.cantidadCuotas = data[0]['cantidadCuotas'];
              $scope.prestamo.montoCuotaQ1 = $filter('number')(data[0]['montoCuotaQ1'], 2);
              $scope.prestamo.montoCuotaQ2 = $filter('number')(data[0]['montoCuotaQ2'], 2);
              $scope.prestamo.fechaDesembolso = data[0]['fechaDesembolso'];
              $scope.prestamo.fechaEntrega = data[0]['fechaEntrega'];
              $scope.prestamo.fechaVencimiento = ''; //data[0][''];
              $scope.prestamo.chequeNo = data[0]['chequeNo'];
              $scope.prestamo.valorGarantizado = $filter('number')(data[0]['valorGarantizado'], 2);
              $scope.prestamo.balance = $filter('number')(data[0]['balance'], 2);


              // if(data[0]['estatus'] == 'P') {
              //   $scope.disabledButton = 'Boton';
              //   $scope.disabledButtonBool = false;
              // } else {
              //   $scope.disabledButton = 'Boton-disabled';
              //   $scope.disabledButtonBool = true;
              // }

            }

          }, 
            (function () {
              $scope.mostrarError('No pudo encontrar el desglose del prestamo #' + prestamo);
            }
          ));
        }
        catch (e) {
          $scope.mostrarError(e);
        }

        $scope.toggleLP();
      }
     

    }])

  //****************************************************
  //CONTROLLERS PRINT DOCUMENT                         *
  //****************************************************
  .controller('ImprimirSolicitudPCtrl', ['$scope', '$filter', '$window', 'DesembolsoElectronicoService', 
                                          function ($scope, $filter, $window, DesembolsoElectronicoService) {
    // $scope.factura = JSON.parse($window.sessionStorage['des']);
    $scope.dataH = {};
    $scope.dataD = [];


  }]);
   

})(_);