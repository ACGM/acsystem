(function (_) {

  angular.module('cooperativa.notadebito', ['ngAnimate'])

    .factory('NotaDebitoService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Nota de Debito
      function guardarND(fecha, ND) {
        var deferred = $q.defer();

        $http.post('/prestamos/nota-de-debito/guardar/', JSON.stringify({'noND': ND.noND, 
                                                                          'fecha': fecha, 
                                                                          'prestamo': ND.prestamo,
                                                                          'valorCapital': ND.valorCapital,
                                                                          'valorInteres': ND.valorInteres,
                                                                          'concepto': ND.concepto})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Eliminar Nota de Debito
      function eliminarND(notaDebitoNo) {
        var deferred = $q.defer();

        $http.post('/facturacion/eliminar/', JSON.stringify({'facturaNo': facturaNo})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Impresion de Nota de Debito (incrementa el campo de IMPRESA)
      function impresionND(fact) {
        var deferred = $q.defer();

        $http.post('/facturacion/print/{factura}/'.replace('{factura}',fact), {'factura': fact}).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Llenar el listado de Notas de Debito
      function all() {
        var deferred = $q.defer();

        $http.get('/api/notasdebito/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un documento en especifico (Desglose)
      function DocumentoById(NoND) {
        var deferred = $q.defer();
        var doc = NoND != undefined? NoND : 0;

        $http.get('/notadebitojson/?noND={NoND}&format=json'.replace('{NoND}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un numero de documento en especifico en listado de documentos
      function byNoND(NoND) {
        var deferred = $q.defer();
        all().then(function (data) {
          var result = data.filter(function (documento) {
            return documento.id == NoND;
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


      return {
        all: all,
        byPosteo: byPosteo,
        byNoND: byNoND,
        guardarND: guardarND,
        DocumentoById: DocumentoById,
        impresionND: impresionND,
        eliminarND : eliminarND
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('NotaDebitoCtrl', ['$scope', '$filter', '$window', 'appService', 'NotaDebitoService',
                                        function ($scope, $filter, $window, appService, NotaDebitoService) {
      
      //Inicializacion de variables
      $scope.disabledButton = 'Boton-disabled';
      $scope.disabledButtonBool = true;
      $scope.posteof = '*';
      $scope.errorShow = false;
      $scope.showLND = true;
      $scope.regAll = false;
      $scope.tableProducto = false;
      $scope.tableSocio = false;

      $scope.item = {};
      $scope.notasdebito = {};

      $scope.ndSeleccionadas = [];
      $scope.reg = [];
      $scope.valoresChk = [];
      $scope.dataD = [];

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLND = 'UpArrow';

      
      // Mostrar/Ocultar panel de Listado de Notas de Debito
      $scope.toggleLND = function() {
        $scope.showLND = !$scope.showLND;

        if($scope.showLND === true) {
          $scope.ArrowLND = 'UpArrow';
        } else {
          $scope.ArrowLND = 'DownArrow';
        }
      }

      // Mostrar/Ocultar posteo Contabilidad
      $scope.toggleInfo = function() {
        $scope.showPostear = !$scope.showPostear;
      }

      //Listado de todas las Notas de Debito
      $scope.listadoND = function() {
        $scope.NoFoundDoc = '';
        $scope.ndSeleccionadas = [];
        $scope.valoresChk = [];

        NotaDebitoService.all().then(function (data) {
          $scope.notasdebito = data;
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

      //Guardar Nota de Debito
      $scope.guardaNotaDebito = function($event) {
        $event.preventDefault();

        try {
          if (!$scope.NDForm.$valid) {
            throw "Verifique que todos los campos esten completados correctamente.";
          }

          var fechaP = $scope.ND.fecha.split('/');
          var fechaFormatted = fechaP[2] + '-' + fechaP[1] + '-' + fechaP[0];

          NotaDebitoService.guardarND(fechaFormatted,$scope.ND).then(function (data) {

            if(isNaN(data)) {
              $scope.mostrarError(data);
              throw data;
            }

            $scope.ND.noND = $filter('numberFixedLen')(data, 8)

            $scope.errorShow = false;
            $scope.listadoND();
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

      //Eliminar ND.
      $scope.eliminarND = function($event) {
        $event.preventDefault();

        try {
          NotaDebitoService.eliminarND($scope.dataH.nd).then(function (data) {
            if(data == 1) {
              $scope.errorShow = false;
              $scope.listadoND();
              $scope.nuevaEntrada();
              $scope.toggleLF();
            } else {
              $scope.mostrarError(data);
            }
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      // Visualizar Documento (ND Existente - desglose)
      $scope.FactFullById = function(NoND, usuario) {
        try {

          NotaDebitoService.DocumentoById(NoND).then(function (data) {

            if(data.length > 0) {
              //completar los campos
              $scope.nuevaEntrada();

              $scope.errorMsg = '';
              $scope.errorShow = false;

              $scope.dataH.factura = $filter('numberFixedLen')(NoFact, 8);
              $scope.dataH.fecha = $filter('date')(data[0]['fecha'], 'dd/MM/yyyy');
              $scope.socioCodigo = data[0]['socioCodigo'];
              $scope.socioNombre = data[0]['socioNombre'];
              $scope.dataH.orden = $filter('numberFixedLen')(data[0]['orden'], 8);
              $scope.dataH.terminos = data[0]['terminos'];
              $scope.dataH.vendedor = data[0]['vendedor'];
              $scope.dataH.posteo = data[0]['posteo'];
              $scope.dataH.impresa = data[0]['impresa'];
              $scope.dataH.borrado = data[0]['borrado'];
              $scope.dataH.borradoPor = data[0]['borradoPor'];
              $scope.dataH.borradoFecha = data[0]['borradoFecha'];

              data[0]['productos'].forEach(function (item) {
                $scope.dataD.push(item);
                $scope.dataH.almacen = item['almacen'];
              })
              $scope.calculaTotales();

              if(data[0]['orden'] > 0) {
                $rootScope.clearOrden();
                $rootScope.FullOrden(data[0]['ordenDetalle']);
              }
            }
          }, 
            (function () {
              $rootScope.mostrarError('No pudo encontrar el desglose del documento #' + NoFact);
            }
          ));
        }
        catch (e) {
          $rootScope.mostrarError(e);
        }
        $scope.toggleLND();
      }

      //Filtrar las Notas de Debito por posteo (SI/NO)
      $scope.filtrarPosteo = function() {
        $scope.ndSeleccionadas = [];
        $scope.valoresChk = [];
        $scope.regAll = false;

        if($scope.posteof != '*') {
          NotaDebitoService.byPosteo($scope.posteof).then(function (data) {
            $scope.notasdebito = data;

            if(data.length > 0){
              $scope.verTodos = '';
            }
        });
        } else {
          $scope.listadoND();
        }        
      }

       //Buscar una nota de credito en especifico
      $scope.filtrarPorNoND = function(NoND) {
        try {
          NotaDebitoService.byNoND(NoND).then(function (data) {
            $scope.notasdebito = data;

            if(data.length > 0) {
              $scope.verTodos = '';
              $scope.NoFoundDoc = '';
            }
          }, 
            (function () {
              $scope.NoFoundDoc = 'No se encontró el documento #' + NoND;
            }
          ));          
        } catch (e) {
          console.log(e);
        }
      }

      //Buscar Documento por ENTER
      $scope.buscarND = function($event, NoND) {
        if($event.keyCode == 13) {
          $scope.filtrarPorNoND(NoND);
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

      //Cuando se le de click al checkbox del header.
      $scope.seleccionAll = function() {
        $scope.ndSeleccionadas = [];

        $scope.notasdebito.forEach(function (data) {
          if (data.posteo == 'N') {
            if ($scope.regAll === true){

              $scope.valoresChk[data.id] = true;
              $scope.ndSeleccionadas.push(data);
            }
            else{

              $scope.valoresChk[data.id] = false;
              $scope.ndSeleccionadas.splice(data);
            }
          }
        });
      }

      //Cuando se le de click a un checkbox de la lista
      $scope.selectedReg = function(iReg) {
        
        index = $scope.notasdebito.indexOf(iReg);

        if ($scope.reg[$scope.notasdebito[index].id] === true){
          $scope.ndSeleccionadas.push($scope.notasdebito[index]);
        }
        else{
          $scope.ndSeleccionadas = _.without($scope.ndSeleccionadas, _.findWhere($scope.ndSeleccionadas, {id : iReg.id}));
        }
      }

      //Nueva Entrada de Factura
      $scope.nuevaEntrada = function(usuario, $event) {
        $scope.ND = {};
        $scope.ND.noND = 0;
        $scope.ND.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

        $scope.showLND = false;
        $scope.ArrowLND = 'DownArrow';

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

  }]);
   
})(_);