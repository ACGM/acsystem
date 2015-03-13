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

      // //Guardar Factura
      // function guardarFact(dataH, dataD) {
      //   var deferred = $q.defer();

      //   $http.post('/facturacion/', JSON.stringify({'cabecera': dataH, 'detalle': dataD})).
      //     success(function (data) {
      //       deferred.resolve(data);
      //     }).
      //     error(function (data) {
      //       deferred.resolve(data);
      //     });

      //   return deferred.promise;
      // }

      // //Impresion de Factura (incrementa el campo de IMPRESA)
      // function impresionFact(fact) {
      //   var deferred = $q.defer();

      //   $http.post('/facturacion/print/{factura}/'.replace('{factura}',fact), {'factura': fact}).
      //     success(function (data) {
      //       deferred.resolve(data);
      //     }).
      //     error(function (data) {
      //       deferred.resolve(data);
      //     });
      //   return deferred.promise;
      // }


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

      return {
        all: all,
        byNoPrestamo : byNoPrestamo,
        PrestamosbySocio : PrestamosbySocio,
        PrestamoById : PrestamoById,
        MarcarPrestamoDC : MarcarPrestamoDC,
        PostearPrestamosOD : PostearPrestamosOD,
        PrestamosPosteados : PrestamosPosteados
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
      $scope.Postear = function($event) {
        $event.preventDefault();

        try {
          MaestraPrestamoService.PostearPrestamosOD($scope.prestamosSeleccionados).then(function (data) {
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

    }])

  //****************************************************
  //CONTROLLERS PRINT DOCUMENT                         *
  //****************************************************
  .controller('ImprimirFacturaCtrl', ['$scope', '$filter', '$window', 'FacturacionService', function ($scope, $filter, $window, FacturacionService) {
    $scope.factura = JSON.parse($window.sessionStorage['factura']);
    $scope.dataH = {};
    $scope.dataD = [];

    FacturacionService.DocumentoById($scope.factura.noFactura).then(function (data) {

      if(data.length > 0) {
        $scope.dataH.factura = $filter('numberFixedLen')($scope.factura.noFactura, 8);
        $scope.dataH.fecha = $filter('date')(data[0]['fecha'], 'dd/MM/yyyy');
        $scope.socioCodigo = data[0]['socioCodigo'];
        $scope.socioNombre = data[0]['socioNombre'];
        $scope.dataH.orden = $filter('numberFixedLen')(data[0]['orden'], 8);
        $scope.dataH.terminos = data[0]['terminos'].replace('CR', 'CREDITO').replace('CO', 'DE CONTADO');
        $scope.dataH.vendedor = data[0]['vendedor'];
      //   $scope.dataH.posteo = data[0]['posteo'];
        $scope.dataH.impresa = data[0]['impresa'];

        data[0]['productos'].forEach(function (item) {
          item.subtotal = parseFloat(item.descuento) > 0? (item.precio * item.cantidad) - ((item.descuento / 100) * item.cantidad * item.precio) : (item.precio * item.cantidad);
          $scope.dataD.push(item);
          // $scope.dataH.almacen = item['almacen'];
        });

        $scope.totalDescuento_ = $scope.totalDescuento();
        $scope.totalValor_ = $scope.totalValor();
      }
    });

    $scope.imprimirFactura = function() {
      console.log('ENTRO');
      // FacturacionService.impresionFact($scope.factura.noFactura).then(function (data) {
      //   console.log(data);
      // });
      // var doc = jsPDF();
      // doc.text(20,20, 'HOLA MUDO');
      // doc.save('pruebaPDF.pdf');
      // console.log(doc);
      $scope.displayClass = 'displayNone';
      console.log($scope.displayClass);
      
      window.print();
      console.log($scope.displayClass);
    }

    $scope.totalValor = function() {
      var total = 0.0;
      var descuento = 0;

      $scope.dataD.forEach(function (item) {
        if(parseFloat(item.descuento) > 0) {
          descuento = (parseFloat(item.descuento)/100);
          descuento = (parseFloat(item.precio) * parseFloat(descuento) * parseFloat(item.cantidad));
        } else {
          descuento = 0;
        }
        total += (parseFloat(item.precio) * parseFloat(item.cantidad)) - descuento;
      });

      return total;
    }

    $scope.totalDescuento = function() {
      var total = 0.0;
      var descuento = 0.0;

      $scope.dataD.forEach(function (item) {
        if(parseFloat(item.descuento) > 0) {
          descuento = (parseFloat(item.descuento)/100);
          descuento = (parseFloat(item.precio) * parseFloat(descuento) * parseFloat(item.cantidad));
        } else {
          descuento = 0;
        }
        total += descuento;
      });

      return total;
    }

    $scope.hora = function() {
      return Date.now();
    }

  }]);
   

})(_);