(function (_) {

  angular.module('cooperativa.notacredito', ['ngAnimate'])

    .factory('NotaCreditoService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Nota de Credito
      function guardarNC(fecha, NC) {
        var deferred = $q.defer();

        $http.post('/prestamos/nota-de-credito/guardar/', JSON.stringify({'noNC': NC.noNC, 
                                                                          'fecha': fecha, 
                                                                          'prestamo': NC.prestamo,
                                                                          'aplicaCuota': NC.AplicadoCuota,
                                                                          'valorCapital': NC.valorCapital.replace(',',''),
                                                                          'valorInteres': NC.valorInteres.replace(',',''),
                                                                          'concepto': NC.concepto})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      // //Eliminar Nota de Credito
      // function eliminarNC(notaCreditoNo) {
      //   var deferred = $q.defer();

      //   $http.post('/facturacion/eliminar/', JSON.stringify({'facturaNo': facturaNo})).
      //     success(function (data) {
      //       deferred.resolve(data);
      //     }).
      //     error(function (data) {
      //       deferred.resolve(data);
      //     });
      //   return deferred.promise;
      // }

      // //Impresion de Nota de Credito (incrementa el campo de IMPRESA)
      // function impresionNC(NC) {
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

      //Llenar el listado de Notas de Credito
      function all() {
        var deferred = $q.defer();

        $http.get('/api/notascredito/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un documento en especifico (Desglose)
      function DocumentoById(NoNC) {
        var deferred = $q.defer();
        var doc = NoNC != undefined? NoNC : 0;

        $http.get('/notadecreditojson/?nonc={NoNC}'.replace('{NoNC}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un numero de prestamo en especifico en listado de documentos
      function byNoPrestamo(NoPrestamo) {
        var deferred = $q.defer();
        all().then(function (data) {
          var result = data.filter(function (documento) {
            return parseFloat(documento.noPrestamo) == parseFloat(NoPrestamo);
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }

      //Buscar un socio en especifico en listado de documentos
      function bySocio(socio) {
        var deferred = $q.defer();
        all().then(function (data) {
          var result = data.filter(function (documento) {
            return documento.getSocio.toLowerCase().substring(0, socio.length) == socio;
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }

      //Buscar por tipo de posteo
      function byPosteo(valor){
        var deferred = $q.defer();

        all().then(function (data) {
          var results = data.filter(function (registros) {
            return registros.posteado == valor;
          });

          if(results.length > 0) {
            deferred.resolve(results);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }

      //*************************************************************************
      //*************************************************************************
      // NOTA DE CREDITO ESPECIAL
      //*************************************************************************
      //*************************************************************************

      //Llenar el listado de Notas de Credito Especiales
      function NotasCreditoEspeciales() {
        var deferred = $q.defer();

        $http.get('/api/notascreditoespecial/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un documento en especifico (Desglose)
      function DocumentoByIdNCE(NoNCE) {
        var deferred = $q.defer();
        var doc = NoNCE != undefined? NoNCE : 0;

        $http.get('/notadecreditoEjson/?nonce={NoNCE}'.replace('{NoNCE}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un numero de orden en especifico en listado de documentos
      function byNoOrdenNCE(NoOrden) {
        var deferred = $q.defer();
        NotasCreditoEspeciales().then(function (data) {
          var result = data.filter(function (documento) {
            return parseFloat(documento.ordenDespacho) == parseFloat(NoOrden);
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }

      //Buscar un socio en especifico en listado de documentos
      function bySocioNCE(socio) {
        var deferred = $q.defer();
        NotasCreditoEspeciales().then(function (data) {
          var result = data.filter(function (documento) {
            return documento.getSocio.toLowerCase().substring(0, socio.length) == socio;
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }

      //Buscar por tipo de posteo
      function byPosteoNCE(valor){
        var deferred = $q.defer();

        NotasCreditoEspeciales().then(function (data) {
          var results = data.filter(function (registros) {
            return registros.posteado == valor;
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
        all             : all,
        byPosteo        : byPosteo,
        byNoPrestamo    : byNoPrestamo,
        bySocio         : bySocio,
        guardarNC       : guardarNC,
        DocumentoById   : DocumentoById,
        // impresionNC     : impresionNC,
        // eliminarNC      : eliminarNC,
        NotasCreditoEspeciales: NotasCreditoEspeciales,
        byPosteoNCE     : byPosteoNCE,
        byNoOrdenNCE    : byNoOrdenNCE,
        bySocioNCE      : bySocioNCE,
        DocumentoByIdNCE: DocumentoByIdNCE
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('NotaCreditoCtrl', ['$scope', '$filter', '$window', 'appService', 'NotaCreditoService', 'MaestraPrestamoService',
                                        function ($scope, $filter, $window, appService, NotaCreditoService, MaestraPrestamoService) {
      
      //Inicializacion de variables
      $scope.disabledButton = 'Boton-disabled';
      $scope.disabledButtonBool = true;
      $scope.errorShow = false;
      $scope.posteof = '*';
      $scope.showLNC = true;

      $scope.tablePrestamo = false;
      $scope.tablePagoCuotas = false;

      $scope.item = {};
      $scope.notascredito = {};

      $scope.dataD = [];

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLNC = 'UpArrow';
      
      //****************************VENTANA SELECCIONAR PRESTAMO**********************************
      // Mostrar/Ocultar table prestamos.
      $scope.PrestamosSel = function() {
        $scope.tablePrestamo = !$scope.tablePrestamo;
        $scope.tablePagoCuotas = false;
      }

      // Prestamos Posteados para llenar table de Prestamos.
      $scope.prestamosFind = function() {
        MaestraPrestamoService.PrestamosPosteados().then(function (data) {
          if(data.length > 0) {
            $scope.prestamos = data;
            $scope.prestamoNoExiste = '';
          } else {
            $scope.prestamoNoExiste = 'No existe prestamo.';
          }

          $scope.tmpPrestamos = data; //Esta variable es para cuando se hagan busqueda de prestamos se mantenga la lista original.
        });
      }

      // Prestamo Seleccionado.
      $scope.selPrestamo = function($event, prestamo) {
        $scope.NC.prestamo = $filter('numberFixedLen') (prestamo.noPrestamo, 9);
        $scope.NC.categoriaPrestamo = prestamo.categoriaPrestamo;
        $scope.NC.socio = prestamo.socio;
        $scope.NC.AplicadoCuota = '';
        $scope.tablePrestamo = false;
      }

      // Buscar prestamo de un socio en especifico.
      $scope.getPrestamoSocio = function($event, datoBuscar) {

        if($event.keyCode == 13) {
          $event.preventDefault();

          if (datoBuscar.length > 0) {
            $scope.prestamos = $scope.tmpPrestamos;

            $scope.prestamos = $scope.prestamos.filter(function (item) {

             if (isNaN(datoBuscar)) {
                return item.socio.toLowerCase().substring(0, datoBuscar.length) == datoBuscar;
              } else {
                return item.noPrestamo == datoBuscar;
              }
            });
          } else {
            $scope.prestamosFind();
          }
          console.log($scope.prestamos);
        }
      }

      // *********************VENTANA PARA SELECCIONAR CUOTA********************************
      // Mostrar/Ocultar table PagoCuotas.
      $scope.PagoCuotasSel = function($event, NoPrestamo) {
        $scope.tablePagoCuotas = !$scope.tablePagoCuotas;

        if($scope.tablePagoCuotas == true) {
          $scope.PagoCuotasFind(parseFloat(NoPrestamo));
        }
      }

      // Pagos de cuotas correspondientes al prestamo seleccionado.
      $scope.PagoCuotasFind = function(NoPrestamo) {
        MaestraPrestamoService.PagoCuotasPrestamosByNoPrestamo(NoPrestamo).then(function (data) {
          if(data.length > 0) {

            $scope.pagoCuotas = data;
            $scope.pagoCuotasNoExiste = '';
          } else {
            alert('No existen pagos de cuotas');
            $scope.pagoCuotasNoExiste = 'No existen pagos de cuotas.';
          }
        });
      }
 
      // PagoCuota Seleccionado.
      $scope.selPagoCuota = function($event, cuota) {
        $scope.NC.AplicadoCuota = $filter('numberFixedLen') (cuota.id, 0);
        $scope.NC.valorCapital = $filter('number')(cuota.valorCapital, 2);
        $scope.NC.valorInteres = $filter('number')(cuota.valorInteres, 2);
        $scope.tablePagoCuotas = false;

      }

      // Mostrar/Ocultar panel de Listado de Notas de Credito
      $scope.toggleLNC = function() {
        $scope.showLNC = !$scope.showLNC;

        if($scope.showLNC === true) {
          $scope.ArrowLNC = 'UpArrow';
        } else {
          $scope.ArrowLNC = 'DownArrow';
        }
      }

      // Mostrar/Ocultar posteo Contabilidad
      $scope.toggleInfo = function() {
        $scope.showPostear = !$scope.showPostear;
      }

      //Listado de todas las Notas de Credito
      $scope.listadoNC = function() {
        $scope.NoFoundDoc = '';

        NotaCreditoService.all().then(function (data) {
          $scope.notascredito = data;

          if(data.length > 0) {
            $scope.verTodos = 'ver-todos-ei';
          }
        });
      }

      //Guardar Nota de Credito
      $scope.guardaNotaCredito = function($event) {
        $event.preventDefault();

        try {
          if (!$scope.NCForm.$valid) {
            throw "Verifique que todos los campos esten completados correctamente.";
          }

          var fechaP = $scope.NC.fecha.split('/');
          var fechaFormatted = fechaP[2] + '-' + fechaP[1] + '-' + fechaP[0];

          NotaCreditoService.guardarNC(fechaFormatted, $scope.NC).then(function (data) {

            if(isNaN(data)) {
              $scope.mostrarError(data);
              throw data;
            }

            $scope.NC.noNC = $filter('numberFixedLen')(data, 8)

            $scope.errorShow = false;
            $scope.listadoNC();
            $scope.showLNC = true;
          },
            (function () {
              $scope.mostrarError('Hubo un error. Contacte al administrador del sistema.');
            }
          ));
        }
        catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Eliminar NC.
      // $scope.eliminarNC = function($event) {
      //   $event.preventDefault();

      //   try {
      //     NotaCreditoService.eliminarNC($scope.dataH.nc).then(function (data) {
      //       if(data == 1) {
      //         $scope.errorShow = false;
      //         $scope.listadoNC();
      //         $scope.nuevaEntrada();
      //         $scope.toggleLNC();
      //       } else {
      //         $scope.mostrarError(data);
      //       }
      //     });
      //   } catch (e) {
      //     $scope.mostrarError(e);
      //   }
      // }

      // Visualizar Documento (NC Existente - desglose)
      $scope.NCFullById = function(NoNC, usuario) {
        try {

          NotaCreditoService.DocumentoById(NoNC).then(function (data) {
            if(data.length > 0) {
              //completar los campos
              $scope.nuevaEntrada();

              $scope.errorMsg = '';
              $scope.errorShow = false;

              $scope.NC.noNC = $filter('numberFixedLen')(NoNC, 8);
              $scope.NC.fecha = $filter('date')(data[0]['fecha'], 'dd/MM/yyyy');
              $scope.NC.AplicadoCuota = data[0]['aplicadoACuota'];
              $scope.NC.prestamo = $filter('numberFixedLen') (data[0]['noPrestamo'], 9);
              $scope.NC.valorCapital = $filter('number')(data[0]['valorCapital'],2);
              $scope.NC.valorInteres = $filter('number')(data[0]['valorInteres'],2);
              $scope.NC.concepto = data[0]['concepto'];
              $scope.NC.socio = data[0]['socio'];
              $scope.NC.categoriaPrestamo = data[0]['categoriaPrestamo'];
            }
          }, 
            (function () {
              $scope.mostrarError('No pudo encontrar el desglose del documento #' + NoNC);
            }
          ));
        }
        catch (e) {
          $scope.mostrarError(e);
        }
        $scope.toggleLNC();
      }

      //Filtrar las Notas de Debito por posteo (SI/NO)
      $scope.filtrarPosteo = function() {

        if($scope.posteof != '*') {
          NotaCreditoService.byPosteo($scope.posteof).then(function (data) {
            $scope.notascredito = data;

            if(data.length > 0){
              $scope.verTodos = '';
            }
        });
        } else {
          $scope.listadoNC();
        }        
      }

      //Buscar un prestamo en especifico
      $scope.filtrarPorNoPrestamo = function($event, NoPrestamo) {
        try {
          if($event.keyCode == 13) {
            NotaCreditoService.byNoPrestamo(NoPrestamo).then(function (data) {
              $scope.notascredito = data;

              if(data.length > 0) {
                $scope.verTodos = '';
                $scope.NoFoundDoc = '';
              }
            }, 
              (function () {
                $scope.NoFoundDoc = 'No se encontró el prestamo #' + NoPrestamo;
              }
            ));          
          }
        } catch (e) {
          console.log(e);
        }
      }

      //Buscar un socio en especifico
      $scope.filtrarPorSocio = function($event, socio) {
        try {
          if($event.keyCode == 13) {
            NotaCreditoService.bySocio(socio).then(function (data) {
              $scope.notascredito = data;

              if(data.length > 0) {
                $scope.verTodos = '';
                $scope.NoFoundDoc = '';
              }
            }, 
              (function () {
                $scope.NoFoundDoc = 'No se encontró el socio ' + socio;
              }
            ));          
          }
        } catch (e) {
          console.log(e);
        }
      }

      // Mostrar/Ocultar error
      $scope.toggleError = function() {
        $scope.errorShow = !$scope.errorShow;
      }

      // Funcion para mostrar error por pantalla
      $scope.mostrarError = function(error) {
        $scope.errorMsg = error;
        $scope.errorShow = true;
        // $timeout($scope.toggleError(), 3000);
      }

      //Nueva Entrada de Nota de Credito
      $scope.nuevaEntrada = function(usuario, $event) {
        $scope.NC = {};
        $scope.NC.noNC = 0;
        $scope.NC.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

        $scope.showLNC = false;
        $scope.ArrowLNC = 'DownArrow';

        $scope.disabledButton = 'Boton';
        $scope.disabledButtonBool = false;

        return false;
      }

      // Agregar una cuenta
      $scope.addCuentaContable = function($event, cuenta) {
        $event.preventDefault();
        var desgloseCuenta = new Object();

        desgloseCuenta.cuenta = cuenta.codigo;
        desgloseCuenta.descripcion = cuenta.descripcion;
        desgloseCuenta.ref = $scope.desgloseCuentas[$scope.desgloseCuentas.length-1].ref;
        desgloseCuenta.debito = 0;
        desgloseCuenta.credito = 0;

        $scope.desgloseCuentas.push(desgloseCuenta);
        $scope.tableCuenta = false;
      }

      $scope.quitarCC = function(desgloseC) {
        if($scope.desgloseCuentas.length == 1) {
          $scope.mostrarError("No puede eliminar todas las cuentas. Verifique la configuración de Documentos-Cuentas.")
        } else {
          $scope.desgloseCuentas = _.without($scope.desgloseCuentas, _.findWhere($scope.desgloseCuentas, {cuenta: desgloseC.cuenta}));
        }
      }

      //Funcion para postear los registros seleccionados. (Postear es llevar al Diario)
      $scope.postear = function(){
        var idoc = 0;
        $scope.iDocumentos = 0;
        $scope.totalDebito = 0.00;
        $scope.totalCredito = 0.00;

        $scope.showPostear = true;
        $scope.desgloseCuentas = [];

        appService.getDocumentoCuentas('NDCR').then(function (data) {
          $scope.documentoCuentas = data;
  
          //Prepara cada linea de posteo
          $scope.facturasSeleccionadas.forEach(function (item) {
            $scope.documentoCuentas.forEach(function (documento) {
              var desgloseCuenta = new Object();
              if (documento.accion == 'D') {
                $scope.totalDebito += parseFloat(item.totalGeneral.toString().replace('$','').replace(',',''));
              } else {
                $scope.totalCredito += parseFloat(item.totalGeneral.toString().replace('$','').replace(',',''));
              }

              desgloseCuenta.cuenta = documento.getCuentaCodigo;
              desgloseCuenta.descripcion = documento.getCuentaDescrp;
              desgloseCuenta.ref = documento.getCodigo + item.id;
              desgloseCuenta.debito = documento.accion == 'D'? item.totalGeneral.toString().replace('$','') : $filter('number')(0.00, 2);
              desgloseCuenta.credito = documento.accion == 'C'? item.totalGeneral.toString().replace('$','') : $filter('number')(0.00, 2);

              $scope.desgloseCuentas.push(desgloseCuenta);
            });
            idoc += 1;
          });
          $scope.iDocumentos = idoc;
        });
      }

      //Imprimir Nota de Debito
      $scope.ImprimirND = function(nd) {
        $window.sessionStorage['notadebito'] = JSON.stringify(nd);
        $window.open('/facturacion/print/{nd}'.replace('{nd}',nd.noND), target='_blank'); 
      }

    }])

  //****************************************************
  //CONTROLLERS PRINT DOCUMENT                         *
  //****************************************************
  .controller('ImprimirNDCtrl', ['$scope', '$filter', '$window', 'NotaDebitoService', function ($scope, $filter, $window, NotaDebitoService) {
    $scope.notadebito = JSON.parse($window.sessionStorage['nd']);
    $scope.dataH = {};
    $scope.dataD = [];

    NotaDebitoService.DocumentoById($scope.notadebito.noND).then(function (data) {

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

    $scope.imprimirND = function() {

      NotaDebitoService.impresionND($scope.notadebito.noND).then(function (data) {
        console.log("DATA: " + data);

        document.getElementById('printBoton').style.display = "None";
        window.print();
        window.location.reload();
        document.getElementById('printBoton').style.display = "";
      });
    }

    $scope.hora = function() {
      return Date.now();
    }

  }])


  //****************************************************
  //CONTROLLERS   (2)                                  *
  //****************************************************
  .controller('NotaCreditoEspecialCtrl', ['$scope', '$filter', '$window', 'appService', 'NotaCreditoService', 'SolicitudOrdenDespachoService',
                                      function ($scope, $filter, $window, appService, NotaCreditoService, SolicitudOrdenDespachoService) {
    
    //Inicializacion de variables
    $scope.disabledButton = 'Boton-disabled';
    $scope.disabledButtonBool = true;
    $scope.posteof = '*';
    $scope.errorShow = false;
    $scope.showLNCE = true;
    $scope.tableProducto = false;
    $scope.tableSocio = false;

    $scope.item = {};
    $scope.notascreditoE = {};

    $scope.dataD = [];

    $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
    $scope.ArrowLNCE = 'UpArrow';

    
    // Mostrar/Ocultar panel de Listado de Notas de Credito Especial
    $scope.toggleLNCE = function() {
      $scope.showLNCE = !$scope.showLNCE;

      if($scope.showLNCE === true) {
        $scope.ArrowLNCE = 'UpArrow';
      } else {
        $scope.ArrowLNCE = 'DownArrow';
      }
    }

    // Mostrar/Ocultar posteo Contabilidad
    $scope.toggleInfo = function() {
      $scope.showPostear = !$scope.showPostear;
    }

    //Listado de todas las Notas de Credito Especiales
    $scope.listadoNCE = function() {
      $scope.NoFoundDoc = '';

      NotaCreditoService.NotasCreditoEspeciales().then(function (data) {
        $scope.notascreditoE = data;

        if(data.length > 0) {
          $scope.verTodos = 'ver-todos-ei';
        }
      });
    }

    //Obtener Orden de Despacho
    $scope.getOrden = function($event, OrdenNo) {
      if($event.keyCode == 13) {
        SolicitudOrdenDespachoService.SolicitudODById(OrdenNo).then(function (data) {
          if(data.length > 0) {
            $scope.NCE.socioCodigo = data[0]['socioCodigo'];
            $scope.NCE.socioNombre = data[0]['socioNombre'];
            $scope.NCE.montoOrden = $filter('number')(data[0]['netoDesembolsar'], 2);
            $scope.NCE.suplidorCodigo = data[0]['idSuplidor'];
            $scope.NCE.suplidorNombre = data[0]['suplidorNombre'];

            $scope.NCE.OrdenNO = OrdenNo;
            
          } else {
            alert('La orden No. ' + OrdenNo + ' No existe');
          }



          console.log(data);
        });
      }
    }

    //Guardar Nota de Credito Especial
    $scope.guardaNotaCreditoE = function($event) {
      $event.preventDefault();

      try {
        if (!$scope.NCEForm.$valid) {
          throw "Verifique que todos los campos esten completados correctamente.";
        }

        var fechaP = $scope.NCE.fecha.split('/');
        var fechaFormatted = fechaP[2] + '-' + fechaP[1] + '-' + fechaP[0];

        NotaCreditoService.guardarNCE(fechaFormatted, $scope.NCE).then(function (data) {

          if(isNaN(data)) {
            $scope.mostrarError(data);
            throw data;
          }

          $scope.NCE.noNCE = $filter('numberFixedLen')(data, 8)

          $scope.errorShow = false;
          $scope.listadoNCE();
        },
          (function () {
            $scope.mostrarError('Hubo un error. Contacte al administrador del sistema.');
          }
        ));
      }
      catch (e) {
        $scope.mostrarError(e);
      }
    }

    //Eliminar NCE.
    // $scope.eliminarNCE = function($event) {
    //   $event.preventDefault();

    //   try {
    //     NotaCreditoService.eliminarNCE($scope.NCE.noNCE).then(function (data) {
    //       if(data == 1) {
    //         $scope.errorShow = false;
    //         $scope.listadoNCE();
    //         $scope.nuevaEntrada();
    //         $scope.toggleLNCE();
    //       } else {
    //         $scope.mostrarError(data);
    //       }
    //     });
    //   } catch (e) {
    //     $scope.mostrarError(e);
    //   }
    // }

    // Visualizar Documento (NCE Existente - desglose)
    $scope.NCEFullById = function(NoNCE, usuario) {
      try {

        NotaCreditoService.DocumentoByIdNCE(NoNCE).then(function (data) {

          if(data.length > 0) {
            //completar los campos
            $scope.nuevaEntrada();

            $scope.errorMsg = '';
            $scope.errorShow = false;

            $scope.NCE.noNCE = $filter('numberFixedLen')(NoNCE, 8);
            $scope.NCE.fecha = $filter('date')(data[0]['fecha'], 'dd/MM/yyyy');
            $scope.NCE.AplicadoCuota = data[0]['aplicadoACuota'];
            $scope.NC.prestamo = data[0]['noPrestamo'];
            $scope.NC.valorCapital = data[0]['valorCapital'];
            $scope.NC.valorInteres = data[0]['valorInteres'];
            $scope.NC.concepto = data[0]['concepto'];
          }
        }, 
          (function () {
            $rootScope.mostrarError('No pudo encontrar el desglose del documento #' + NoNCE);
          }
        ));
      }
      catch (e) {
        $rootScope.mostrarError(e);
      }
      $scope.toggleLNCE();
    }

    //Filtrar las Notas de Credito Especial por posteo (SI/NO)
    $scope.filtrarPosteo = function() {

      if($scope.posteof != '*') {
        NotaCreditoService.byPosteoNCE($scope.posteof).then(function (data) {
          $scope.notascreditoE = data;

          if(data.length > 0){
            $scope.verTodos = '';
          }
      });
      } else {
        $scope.listadoNCE();
      }        
    }

    //Buscar una orden en especifico
    $scope.filtrarPorNoOrden = function($event, NoOrden) {
      try {
        if($event.keyCode == 13) {
          NotaCreditoService.byNoOrdenNCE(NoOrden).then(function (data) {
            $scope.notascreditoE = data;

            if(data.length > 0) {
              $scope.verTodos = '';
              $scope.NoFoundDoc = '';
            }
          }, 
            (function () {
              $scope.NoFoundDoc = 'No se encontró la orden #' + NoOrden;
            }
          ));          
        }
      } catch (e) {
        console.log(e);
      }
    }

    //Buscar un socio en especifico
    $scope.filtrarPorSocio = function($event, socio) {
      try {
        if($event.keyCode == 13) {
          NotaCreditoService.bySocioNCE(socio).then(function (data) {
            $scope.notascreditoE = data;

            if(data.length > 0) {
              $scope.verTodos = '';
              $scope.NoFoundDoc = '';
            }
          }, 
            (function () {
              $scope.NoFoundDoc = 'No se encontró el socio ' + socio;
            }
          ));          
        }
      } catch (e) {
        console.log(e);
      }
    }

    //Buscar Documento por ENTER
    $scope.buscarNCE = function($event, NoNCE) {
      if($event.keyCode == 13) {
        $scope.filtrarPorNoNCE(NoNCE);
      }
    }

    // Mostrar/Ocultar error
    $scope.toggleError = function() {
      $scope.errorShow = !$scope.errorShow;
    }

    // Funcion para mostrar error por pantalla
    $scope.mostrarError = function(error) {
      $scope.errorMsg = error;
      $scope.errorShow = true;
      // $timeout($scope.toggleError(), 3000);
    }

    //Nueva Entrada de Nota de Credito
    $scope.nuevaEntrada = function(usuario, $event) {
      $scope.NCE = {};
      $scope.NCE.noNCE = 0;
      $scope.NCE.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

      $scope.showLNCE = false;
      $scope.ArrowLNCE = 'DownArrow';

      $scope.disabledButton = 'Boton';
      $scope.disabledButtonBool = false;

      return false;
    }

    // Agregar una cuenta
    $scope.addCuentaContable = function($event, cuenta) {
      $event.preventDefault();
      var desgloseCuenta = new Object();

      desgloseCuenta.cuenta = cuenta.codigo;
      desgloseCuenta.descripcion = cuenta.descripcion;
      desgloseCuenta.ref = $scope.desgloseCuentas[$scope.desgloseCuentas.length-1].ref;
      desgloseCuenta.debito = 0;
      desgloseCuenta.credito = 0;

      $scope.desgloseCuentas.push(desgloseCuenta);
      $scope.tableCuenta = false;
    }

    $scope.quitarCC = function(desgloseC) {
      if($scope.desgloseCuentas.length == 1) {
        $scope.mostrarError("No puede eliminar todas las cuentas. Verifique la configuración de Documentos-Cuentas.")
      } else {
        $scope.desgloseCuentas = _.without($scope.desgloseCuentas, _.findWhere($scope.desgloseCuentas, {cuenta: desgloseC.cuenta}));
      }
    }

    //Funcion para postear los registros seleccionados. (Postear es llevar al Diario)
    $scope.postear = function(){
      var idoc = 0;
      $scope.iDocumentos = 0;
      $scope.totalDebito = 0.00;
      $scope.totalCredito = 0.00;

      $scope.showPostear = true;
      $scope.desgloseCuentas = [];

      appService.getDocumentoCuentas('FACT').then(function (data) {
        $scope.documentoCuentas = data;

        //Prepara cada linea de posteo
        $scope.facturasSeleccionadas.forEach(function (item) {
          $scope.documentoCuentas.forEach(function (documento) {
            var desgloseCuenta = new Object();
            if (documento.accion == 'D') {
              $scope.totalDebito += parseFloat(item.totalGeneral.toString().replace('$','').replace(',',''));
            } else {
              $scope.totalCredito += parseFloat(item.totalGeneral.toString().replace('$','').replace(',',''));
            }

            desgloseCuenta.cuenta = documento.getCuentaCodigo;
            desgloseCuenta.descripcion = documento.getCuentaDescrp;
            desgloseCuenta.ref = documento.getCodigo + item.id;
            desgloseCuenta.debito = documento.accion == 'D'? item.totalGeneral.toString().replace('$','') : $filter('number')(0.00, 2);
            desgloseCuenta.credito = documento.accion == 'C'? item.totalGeneral.toString().replace('$','') : $filter('number')(0.00, 2);

            $scope.desgloseCuentas.push(desgloseCuenta);
          });
          idoc += 1;
        });
        $scope.iDocumentos = idoc;
      });
    }

    //Imprimir Nota de Credito Especial
    $scope.ImprimirNCE = function(nce) {
      $window.sessionStorage['notadebito'] = JSON.stringify(nce);
      $window.open('/facturacion/print/{nd}'.replace('{nd}',nd.noND), target='_blank'); 
    }

  }]);
   
})(_);