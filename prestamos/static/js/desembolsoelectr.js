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

      //Relacionar prestamos con el archivo de banco generado.
      function relacionarPrestamosConArchivoBanco(prestamos, archivoBanco) {
        var deferred = $q.defer();

        $http.post('/prestamos/archivo-banco/set/', JSON.stringify({'prestamos': prestamos, 'archivoBanco': archivoBanco})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      return {
        listadoPrestamos: listadoPrestamos,
        byNoPrestamo: byNoPrestamo,
        PrestamosbySocio: PrestamosbySocio,
        relacionarPrestamosConArchivoBanco: relacionarPrestamosConArchivoBanco
        // PrestamoById: PrestamoById
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('DesembolsoPrestamosCtrl', ['$scope', '$filter', '$timeout', '$window', 'DesembolsoElectronicoService', 'MaestraPrestamoService', 'appService',
                                        function ($scope, $filter, $timeout, $window, DesembolsoElectronicoService, MaestraPrestamoService, appService) {
      
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

      // Funcion para mostrar error por pantalla
      $scope.mostrarError = function(error) {
        $scope.errorMsg = error;
        $scope.errorShow = true;
      }

      // Mostrar/Ocultar error
      $scope.toggleError = function() {
        $scope.errorShow = !$scope.errorShow;
      }

      //Listado de todos los prestamos
      $scope.listadoPrestamos = function() {
        $scope.NoFoundDoc = '';
        $scope.prestamosSeleccionados = [];
        $scope.valoresChk = [];
        $scope.netoTotal = 0;

        DesembolsoElectronicoService.listadoPrestamos().then(function (data) {
          $scope.prestamos = data;
          $scope.regAll = false;

          if(data.length > 0) {
            $scope.verTodos = 'ver-todos-ei';

            var i = 0;
            data.forEach(function (item) {
              $scope.valoresChk[i] = false;
              i++;
              $scope.netoTotal += parseFloat(item['netoDesembolsar']);
            });
          } else {
            $scope.NoFoundDoc = "No existen registros para mostrar.";
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

        try {

          if($scope.prestamosSeleccionados.length == 0) {
            throw "Debe seleccionar al menos un prestamo para esta acción.";
          }

          //Validar que los prestamos seleccionados hayan sido generados en un archivo para el banco.
          $scope.prestamosSeleccionados.forEach(function (item) {
            if(item.fechaDesembolso == null) {
              throw "No puede ejecutar la acción porque el prestamo No. " + $filter('numberFixedLen')(item.noPrestamo, 9) + " no ha sido generado para enviar al banco.";
            }
          })

          MaestraPrestamoService.MarcarPrestamoDC($scope.prestamosSeleccionados, accion).then(function (data) {
            if(data == 1) {
              $scope.listadoPrestamos();
              $scope.errorShow = false;
            } else {
              $scope.mostrarError(data);
            }
          }, function() {
            $scope.mostrarError("Hubo un error interno en la aplicacion, contacte al administrador.");
          })
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Generar archivo para el banco
      $scope.GeneraArchivoBanco = function($event) {
        $event.preventDefault();

        try {

          if($scope.prestamosSeleccionados.length == 0) {
            throw "Debe seleccionar al menos un prestamo para esta acción.";
          }

          //Al metodo principal deben ser pasado los siguientes parametros:
          // 1) tipoServicio (01 Nomina Automatica, 02 Pago a Suplidores, ..., 06 Transferencia a Cta)
          // 2) fechaEfectiva YYYYMMDD
          // 3) cantidadDB
          // 4) montoTotalDB
          // 5) cantidadCR
          // 6) montoTotalCR
          // 7) numeroAfiliacion
          // 8) fechaEnvio YYYYMMDD
          // 9) horaEnvio HHMM
          var totalDB = 0;
          var Cabecera = {};
          var Detalle = [];

          $scope.prestamosSeleccionados.forEach(function (item) {
            totalDB += parseFloat(item.netoDesembolsar);
          });

          Cabecera.tipoServicio = '01';
          Cabecera.fechaEfectiva = $filter('date')(Date.now(), 'yyyyMMdd');
          Cabecera.cantidadDB = $scope.prestamosSeleccionados.length;
          Cabecera.montoTotalDB = $filter('number')(totalDB, 2);
          Cabecera.cantidadCR = 0;
          Cabecera.montoTotalCR = 0;
          Cabecera.numeroAfiliacion = '';
          Cabecera.fechaEnvio = $filter('date')(Date.now(), 'yyyyMMdd');
          Cabecera.horaEnvio = $filter('date')(Date.now(), 'HHmm');

          // Para el registro N son necesarios los siguientes campos
          /*
            1) cuentaDestino
            2) monedaDestino = 214 para peso dominicano
            3) montoTransaccion
            4) codigoSocio / suplidorId
          */
          $scope.prestamosSeleccionados.forEach(function (registroN) {
            var item = {};

            item.cuentaDestino = registroN.socioCuentaBancaria;
            item.monedaDestino = '214';
            item.montoTransaccion = $filter('number')(registroN.netoDesembolsar, 2);
            item.socioCodigo = registroN.socioCodigo;

            item.prestamoNo = registroN.noPrestamo; //Exclusivo para desembolso de prestamos

            Detalle.push(item);
          });
  
          //Enviar para crear registros para archivo.
          appService.generarArchivoBanco(Cabecera, Detalle).then(function (data) {

            DesembolsoElectronicoService.relacionarPrestamosConArchivoBanco($scope.prestamosSeleccionados, data).then(function (data) {
              $scope.listadoPrestamos();

              alert('Fue generado el archivo para banco!');
              $scope.errorShow = false;
            });
          });
        } catch (e) {
          $scope.mostrarError(e);
          console.log(e);
        }
      }

      //Ver archivo de desembolso para Banco
      $scope.verArchivoBanco = function($event, archivoBanco) {
        $event.preventDefault();

        $window.open('/static/media/archivosBanco/{archivoBanco}'.replace('{archivoBanco}', archivoBanco), target='_blank'); 
      }

      //Cuando se le de click al checkbox del header.
      $scope.seleccionAll = function() {
        $scope.prestamosSeleccionados = [];

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

      //Imprimir Listado de Desembolsos
      $scope.imprimirListado = function($event) {
        $window.print();
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

    $scope.dataH = JSON.parse($window.sessionStorage['prestamoRC']);

    var fechaP = $filter('date')(Date.now(), 'dd/MM/yyyy').split('/');
    var fechaF = new Date(fechaP[2] + '/' + fechaP[1] + '/' + fechaP[0]);

    var nextDate = new Date();
    nextDate.setDate(fechaF.getDate()+parseInt($scope.dataH.cuotas * 15));

    $scope.fechaVencimiento = $filter('date')(nextDate, 'dd/MM/yyyy');
    
  }]);
   

})(_);