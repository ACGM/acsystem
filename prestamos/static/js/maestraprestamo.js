(function (_) {

  angular.module('cooperativa.maestraprestamo', ['ngAnimate'])

    // Filtro para manejo de bloqueo de seleccion de prestamo segun el estatus (checkbox)
    .filter('posteoMP', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('E', false)
                .replace('D', false)
                .replace('C', false)
                .replace('P', true)
                .replace('S', true);
        return input;
      }
    })

    // Filtro para imagenes a mostrar por cada estatus del prestamo.
    .filter('OpenCloseMP', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('E', 'icon-folder-open')
                .replace('P', 'icon-folder')
                .replace('S', 'icon-folder')
                .replace('C', 'icon-banknote')
                .replace('D', 'icon-coin');
        return input;
      }
    })

    .factory('MaestraPrestamoService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Cambios Prestamo
      function guardarCambios(prestamo) {
        var deferred = $q.defer();

        $http.post('/prestamos/maestra/cambios/', JSON.stringify({'noPrestamo': prestamo.noPrestamo,
                                                                  'tipoNomina': prestamo.tipoNomina,
                                                                  'montoQ1': prestamo.montoQ1,
                                                                  'montoQ2': prestamo.montoQ2})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Llenar el listado de prestamos
      function all() {
        var deferred = $q.defer();

        $http.get('/api/prestamos/maestra/listado/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Marcar Prestamo como Desembolso Electronico o Cheque.
      function MarcarPrestamoDC(prestamos, accion) {
        var deferred = $q.defer();

        $http.post('/prestamos/maestra/marcarcomo/', JSON.stringify({'prestamos': prestamos, 'accion': accion})). 
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un prestamo en especifico (Desglose)
      function PrestamoById(NoPrestamo) {
        var deferred = $q.defer();
        var doc = NoPrestamo != undefined? NoPrestamo : 0;

        $http.get('/maestraPrestamojson/?noprestamo={NoPrestamo}&format=json'.replace('{NoPrestamo}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un numero de prestamo en especifico en listado de prestamos
      function byNoPrestamo(NoPrestamo) {
        var deferred = $q.defer();
        all().then(function (data) {
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

        all().then(function (data) {
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

      // Marcar prestamos como posteados.
      function PostearPrestamosOD(prestamos) {
        var deferred = $q.defer();

        $http.post('/maestraPrestamos/prestamosOD/postear/', JSON.stringify({'prestamos': prestamos})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Prestamos/OD posteados.
      function PrestamosPosteados() {
        var deferred = $q.defer();
        all().then(function (data) {
          var result = data.filter(function (documento) {
            console.log(documento)
            return documento.estatus == 'P';
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }

      //Buscar los prestamos de un socio (prestamos aprobados)
      function prestamosDetalleByCodigoSocio(socio) {
        var deferred = $q.defer();

        $http.get('/api/prestamos/maestra/socio/detalle/{socio}/?format=json'.replace('{socio}', socio))
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar los balances de prestamos de un socio (undefined = todos)
      function prestamosBalanceByCodigoSocio(socio) {
        var deferred = $q.defer();

        if(socio == undefined) {
          url = '/api/prestamos/maestra/socio/balance/?format=json';
        } else {
          url = '/api/prestamos/maestra/socio/balance/{socio}/?format=json'.replace('{socio}', socio);
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Pagos Cuotas de Prestamos
      function PagoCuotasPrestamosByNoPrestamo(NoPrestamo) {
        var deferred = $q.defer();

        if(NoPrestamo != undefined) {
          url = '/prestamos/pago-cuotas/{NoPrestamo}/?format=json'.replace('{NoPrestamo}', NoPrestamo);
        } else {
          url = '/prestamos/pago-cuotas/?format=json';
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      return {
        all: all,
        byNoPrestamo : byNoPrestamo,
        PrestamosbySocio : PrestamosbySocio,
        PrestamoById : PrestamoById,
        MarcarPrestamoDC : MarcarPrestamoDC,
        PostearPrestamosOD : PostearPrestamosOD,
        PrestamosPosteados : PrestamosPosteados,
        guardarCambios : guardarCambios,
        prestamosDetalleByCodigoSocio : prestamosDetalleByCodigoSocio,
        prestamosBalanceByCodigoSocio : prestamosBalanceByCodigoSocio,
        PagoCuotasPrestamosByNoPrestamo : PagoCuotasPrestamosByNoPrestamo
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('MaestraPrestamosCtrl', ['$scope', '$filter', '$timeout', '$window', 'MaestraPrestamoService', 
                                        function ($scope, $filter, $timeout, $window, MaestraPrestamoService) {
      
      //Inicializacion de variables
      $scope.disabledButton = 'Boton-disabled';
      $scope.disabledButtonBool = true;
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

      panelesSize();

      window.onresize = function(event) {
        panelesSize();
      }

      function panelesSize() {
        document.getElementById('prestamosContainer').style.height = (window.innerHeight - 280) + 'px';
      }

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

      //Listado de todos los prestamos
      $scope.listadoPrestamos = function() {
        $scope.NoFoundDoc = '';
        $scope.prestamosSeleccionados = [];
        $scope.valoresChk = [];

        MaestraPrestamoService.all().then(function (data) {
          $scope.prestamos = data;
          
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

      //Guardar Cambios en Prestamo Seleccionado.
      $scope.GuardarCambiosPrestamo = function($event) {
        var prestamo = {};

        prestamo.noPrestamo = $scope.dataH.noPrestamo;
        prestamo.tipoNomina = $scope.dataH.tipoPrestamoNomina;
        prestamo.montoQ1 = $scope.prestamo.montoCuotaQ1;
        prestamo.montoQ2 = $scope.prestamo.montoCuotaQ2;

        MaestraPrestamoService.guardarCambios(prestamo).then(function (data) {
          if(data == 1) {
            $scope.PrestamoFullById($event, $scope.dataH.noPrestamo);
            alert('Los cambios fueron guardados.');
          } else {
            $scope.mostrarError(data);
          }
        })

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
              console.log(data);

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
              $scope.dataH.socioDepartamento = data[0]['socioDepartamento'];
              $scope.dataH.oficial = data[0]['oficial'];
              $scope.dataH.localidad = data[0]['localidad'];
              $scope.dataH.estatus = data[0]['estatus'];
              $scope.dataH.posteadoFecha = data[0]['posteadoFecha'];
              $scope.dataH.tipoPrestamoNomina = data[0]['tipoPrestamoNomina'];

              $scope.prestamo.noSolicitud = $filter('numberFixedLen')(solicitudNo, 8);
              $scope.prestamo.monto = $filter('number')(data[0]['montoInicial'], 2);
              $scope.prestamo.tasaInteresAnual = data[0]['tasaInteresAnual'];
              $scope.prestamo.tasaInteresMensual = data[0]['tasaInteresMensual']/2;
              $scope.prestamo.tasaInteresPrestBaseAhorro = data[0]['tasaInteresPrestBaseAhorro']/2;
              $scope.prestamo.pagoPrestamoAnterior = data[0]['pagoPrestamoAnterior'];
              $scope.prestamo.cantidadCuotas = data[0]['cantidadCuotas'];
              $scope.prestamo.montoCuotaQ1 = $filter('number')(data[0]['montoCuotaQ1'], 2);
              $scope.prestamo.montoCuotaQ2 = $filter('number')(data[0]['montoCuotaQ2'], 2);
              $scope.prestamo.fechaDesembolso = data[0]['fechaDesembolso'];
              $scope.prestamo.fechaEntrega = data[0]['fechaEntrega'];
              $scope.prestamo.chequeNo = data[0]['chequeNo'];
              $scope.prestamo.valorGarantizado = $filter('number')(data[0]['valorGarantizado'], 2);
              $scope.prestamo.valorAhorro = $filter('number')(data[0]['valorAhorro'], 2);
              $scope.prestamo.balance = $filter('number')(data[0]['balance'], 2);

              $scope.prestamo.valorInteresGarantizado = $filter('number')(data[0]['valorGarantizado'] * (data[0]['tasaInteresMensual']/data[0]['quincenas']/100), 2);
              $scope.prestamo.valorInteresAhorro = $filter('number')(data[0]['valorAhorro'] * (data[0]['tasaInteresPrestBaseAhorro']/data[0]['quincenas']/100), 2)

              var fechaP = $filter('date')(Date.now(), 'dd/MM/yyyy').split('/');
              var fechaF = new Date(fechaP[2] + '/' + fechaP[1] + '/' + fechaP[0]);

              var nextDate = new Date();
              nextDate.setDate(fechaF.getDate()+parseInt($scope.prestamo.cantidadCuotas * 15));

              $scope.prestamo.fechaVencimiento = $filter('date')(nextDate, 'dd/MM/yyyy');


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

        if($scope.showLP == true) {
          $scope.toggleLP();
        }
      }

      //Marcar Prestamo como Cheque
      $scope.marcarPrestamoDC = function(prestamo, accion) {
        var p = [];
        p.push(prestamo);

        MaestraPrestamoService.MarcarPrestamoDC(p, accion).then(function (data) {
          if(data == 1) {
            $scope.listadoPrestamos();
          } else {
            $scope.mostrarError(data);
          }
        }, function() {
          $scope.mostrarError("Hubo un error interno en la aplicacion, contacte al administrador.");
        })
      }

      //Postear Prestamos/OD
      $scope.Postear = function($event, prestamoOD) {
        $event.preventDefault();

        try {
          console.log(prestamoOD)

          var p = [];
          p.push (prestamoOD);

          MaestraPrestamoService.PostearPrestamosOD(p).then(function (data) {
            if(data == 1) {
              $scope.listadoPrestamos();
            } else {
              $scope.mostrarError(data);
            }

          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Cuando se le de click al checkbox del header.
      $scope.seleccionAll = function() {

        $scope.prestamos.forEach(function (data) {
          if (data.estatus == 'E') {

            if ($scope.regAll === true){
              $scope.valoresChk[data.noPrestamo] = true;
              $scope.prestamosSeleccionados.push(data);
            }
            else{
              $scope.valoresChk[data.noPrestamo] = false;
              $scope.prestamosSeleccionados.splice(data);
            }
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

    }]);  

})(_);