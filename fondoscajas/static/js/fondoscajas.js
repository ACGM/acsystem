(function (_) {

  angular.module('cooperativa.fondoscajas', ['ngAnimate'])

    .factory('FondosCajasService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Desembolso Caja
      function guardaDesembolso(dataH, dataD) {
        var deferred = $q.defer();

        $http.post('/desembolso/', JSON.stringify({'cabecera': dataH, 'detalle': dataD})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Llenar el listado de Desembolsos
      function all() {
        var deferred = $q.defer();

        $http.get('/api/desembolsos/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Traer los distritos
      function distritos() {
        var deferred = $q.defer();

        $http.get('/api/distritos/?format=json')
          .success(function (data) {
              deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Buscar un numero de cheque en especifico en listado de documentos
      function byNoCheque(NoCheque) {
        var deferred = $q.defer();
        all().then(function (data) {
          var result = data.filter(function (registro) {
            return registro.cheque == NoCheque;
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }


      //Buscar un desembolso en especifico (Desglose)
      function DocumentoById(NoCheque) {
        var deferred = $q.defer();
        var doc = NoCheque != undefined? NoCheque : 0;

        $http.get('/desembolsojson/?nocheque={NoCheque}&format=json'.replace('{NoCheque}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }


      return {
        all: all,
        distritos: distritos,
        guardaDesembolso: guardaDesembolso,
        byNoCheque: byNoCheque,
        DocumentoById: DocumentoById
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('DesembolsosCajasCtrl', ['$scope', '$filter', 'FondosCajasService', 
                                        function ($scope, $filter, FondosCajasService) {
      
      //Inicializacion de variables
      $scope.showLD = true;
      $scope.regAll = false;

      $scope.item = {};
      $scope.desembolsos = {};

      $scope.desembolsosSeleccionadas = [];
      $scope.reg = [];
      $scope.valoresChk = [];
      $scope.dataD = [];

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLD = 'UpArrow';

      
      // Mostrar/Ocultar panel de Listado de Desembolsos
      $scope.toggleLD = function() {
        $scope.showLD = !$scope.showLD;

        if($scope.showLD === true) {
          $scope.ArrowLD = 'UpArrow';
        } else {
          $scope.ArrowLD = 'DownArrow';
        }
      }

      //Listado de todos los desembolsos
      $scope.listadoDesembolsos = function() {
        $scope.desembolsosSeleccionadas = [];
        $scope.valoresChk = [];

        FondosCajasService.all().then(function (data) {
          $scope.desembolsos = data;
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

      //Buscar un cheque en especifico
      $scope.filtrarPorNoCheque = function(NoCheque) {
        try {
          FondosCajasService.byNoCheque(NoCheque).then(function (data) {
            $scope.desembolsos = data;

            if(data.length > 0) {
              $scope.verTodos = '';
              $scope.NoFoundDoc = '';
            }
          }, 
            (function () {
              $scope.NoFoundDoc = 'No se encontró el cheque #' + NoCheque;
            }
          ));          
        } catch (e) {
          console.log(e);
        }
      }

      //Buscar Cheque por ENTER
      $scope.buscarCheque = function($event, NoCheque) {
        if($event.keyCode == 13) {
          $scope.filtrarPorNoCheque(NoCheque);
        }
      }

      // //Guardar Factura
      // $scope.guardarFactura = function($event) {
      //   $event.preventDefault();

      //   try {
      //     if (!$scope.FacturaForm.$valid) {
      //       throw "Verifique que todos los campos esten completados correctamente.";
      //     }

      //     var fechaP = $scope.dataH.fecha.split('/');
      //     var fechaFormatted = fechaP[2] + '-' + fechaP[1] + '-' + fechaP[0];

      //     var dataH = new Object();

      //     dataH.factura = $scope.dataH.factura != undefined? $scope.dataH.factura : 0;
      //     dataH.fecha = fechaFormatted;
      //     dataH.terminos = $scope.dataH.terminos;
      //     dataH.vendedor = $scope.dataH.vendedor;
      //     dataH.almacen = $scope.dataH.almacen;
      //     dataH.socio = $scope.socioCodigo != undefined? $scope.socioCodigo : null;
      //     dataH.orden = $scope.orden != undefined? $scope.orden : null;

      //     if ($scope.dataD.length == 0) {
      //       throw "Debe agregar un producto al menos.";
      //     }

      //     FacturacionService.guardarFact(dataH,$scope.dataD).then(function (data) {
      //       $rootScope.factura = data;
      //       $scope.dataH.factura = $filter('numberFixedLen')(data, 8)

      //       $scope.errorShow = false;
      //       $scope.listadoFacturas();

      //       //SI ES A CREDITO LA FACTURA SE DEBE CREAR UNA ORDEN DE DESPACHO SUPERRCOOP
      //       if($scope.dataH.terminos == "CR") {

      //         $scope.mostrarOrden(true);
      //         $scope.disabledButton = 'Boton-disabled';
      //         $scope.disabledButtonBool = true;
      //         $scope.BotonOrden = 'BotonOrden';

      //         $rootScope.total = $scope.total;
      //         $rootScope.getCategoriaPrestamo($scope.dataH.vendedor);

      //         if ($rootScope.oid > 0) {
      //           $rootScope.guardarOrden($event);
      //         }

      //         } else {              
      //           $scope.nuevaEntrada();
      //           $scope.toggleLF();
      //         }
      //     },
      //     (function () {
      //       $rootScope.mostrarError('Hubo un error. Contacte al administrador del sistema.');
      //     }
      //     ));

      //   }
      //   catch (e) {
      //     $rootScope.mostrarError(e);
      //   }
      // }

      // // Visualizar Documento (Factura Existente - desglose)
      // $scope.FactFullById = function(NoFact, usuario) {
      //   try {
      //     FacturacionService.DocumentoById(NoFact).then(function (data) {

      //       if(data.length > 0) {
      //         $scope.errorMsg = '';
      //         $scope.errorShow = false;

      //         //completar los campos
      //         $scope.nuevaEntrada();

      //         $scope.dataH.factura = $filter('numberFixedLen')(NoFact, 8);
      //         $scope.dataH.fecha = $filter('date')(data[0]['fecha'], 'dd/MM/yyyy');
      //         $scope.socioCodigo = data[0]['socioCodigo'];
      //         $scope.socioNombre = data[0]['socioNombre'];
      //         $scope.dataH.orden = $filter('numberFixedLen')(data[0]['orden'], 8);
      //         $scope.dataH.terminos = data[0]['terminos'];
      //         $scope.dataH.vendedor = data[0]['vendedor'];
      //         $scope.dataH.posteo = data[0]['posteo'];

      //         data[0]['productos'].forEach(function (item) {
      //           $scope.dataD.push(item);
      //           $scope.dataH.almacen = item['almacen'];
      //         })
      //         $scope.calculaTotales();

      //         if(data[0]['orden'] > 0) {
      //           $rootScope.clearOrden();
      //           $rootScope.FullOrden(data[0]['ordenDetalle']);
      //         }
      //       }

      //     }, 
      //       (function () {
      //         $rootScope.mostrarError('No pudo encontrar el desglose del documento #' + NoFact);
      //       }
      //     ));
      //   }
      //   catch (e) {
      //     $rootScope.mostrarError(e);
      //   }

      //   $scope.toggleLF();
      // }


      // //Eliminar producto de la lista de entradas
      // $scope.delProducto = function($event, prod) {
      //   $event.preventDefault();
      //   try {
      //     $scope.dataD = _.without($scope.dataD, _.findWhere($scope.dataD, {codigo: prod.codigo}));

      //     $scope.calculaTotales();
          
      //   } catch (e) {
      //     $rootScope.mostrarError(e);
      //   }
      // }

      // //Traer almacenes
      // $scope.getAlmacenes = function() {
      //   InventarioService.almacenes().then(function (data) {
      //     $scope.almacenes = data;
      //   });
      // }

      // //Filtrar las facturas por posteo (SI/NO)
      // $scope.filtrarPosteo = function() {
      //   $scope.facturasSeleccionadas = [];
      //   $scope.valoresChk = [];
      //   $scope.regAll = false;

      //   if($scope.posteof != '*') {
      //     FacturacionService.byPosteo($scope.posteof).then(function (data) {
      //       $scope.facturas = data;

      //       if(data.length > 0){
      //         $scope.verTodos = '';
      //       }
      //   });
      //   } else {
      //     $scope.listadoFacturas();
      //   }        
      // }

      //  //Buscar una factura en especifico
      // $scope.filtrarPorNoFact = function(NoFact) {
      //   try {
      //     FacturacionService.byNoFact(NoFact).then(function (data) {
      //       $scope.facturas = data;

      //       if(data.length > 0) {
      //         $scope.verTodos = '';
      //         $scope.NoFoundDoc = '';
      //       }
      //     }, 
      //       (function () {
      //         $scope.NoFoundDoc = 'No se encontró el documento #' + NoFact;
      //       }
      //     ));          
      //   } catch (e) {
      //     console.log(e);
      //   }
      // }

      // //Buscar Documento por ENTER
      // $scope.buscarFact = function($event, NoFact) {
      //   if($event.keyCode == 13) {
      //     $scope.filtrarPorNoFact(NoFact);
      //   }
      // }

      // // Mostrar/Ocultar error
      // $scope.toggleError = function() {
      //   $scope.errorShow = !$scope.errorShow;
      // }

      // // Funcion para mostrar error por pantalla
      // $rootScope.mostrarError = function(error) {
      //   $scope.errorMsg = error;
      //   $scope.errorShow = true;
      // }

      // //Cuando se le de click al checkbox del header.
      // $scope.seleccionAll = function() {

      //   $scope.facturas.forEach(function (data) {
      //     if (data.posteo == 'N') {
      //       if ($scope.regAll === true){

      //         $scope.valoresChk[data.id] = true;
      //         $scope.facturasSeleccionadas.push(data);
      //       }
      //       else{

      //         $scope.valoresChk[data.id] = false;
      //         $scope.facturasSeleccionadas.splice(data);
      //       }
      //     }

      //   });
      // }

      
      // //Cuando se le de click a un checkbox de la lista
      // $scope.selectedReg = function(iReg) {
        
      //   index = $scope.facturas.indexOf(iReg);

      //   if ($scope.reg[$scope.facturas[index].id] === true){
      //     $scope.facturasSeleccionadas.push($scope.facturas[index]);
      //   }
      //   else{

      //     $scope.facturasSeleccionadas.splice($scope.facturasSeleccionadas[index],1);
      //   }
      // }

      // //Nueva Entrada de Factura
      // $scope.nuevaEntrada = function(usuario) {
      //   $scope.producto = '';
      //   $scope.almacen = '';
      //   $scope.subtotal = '';
      //   $scope.descuento = '';
      //   $scope.total = '';

      //   $scope.socioCodigo = '';
      //   $scope.socioNombre = '';
        
      //   $scope.dataH = {};
      //   $scope.dataD = [];
      //   $scope.productos = [];

      //   $rootScope.mostrarOrden(false);
      //   $scope.showLF = false;
      //   $scope.ArrowLF = 'DownArrow';
      //   $scope.BotonOrden = '';
      //   $scope.dataH.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      //   $scope.dataH.vendedor = usuario;
      //   $scope.dataH.terminos = 'CO';
      //   $scope.dataH.posteo = 'N';

      //   $scope.disabledButton = 'Boton';
      //   $scope.disabledButtonBool = false;

      // }


      // //Traer productos
      // $scope.getProducto = function($event) {
      //   $event.preventDefault();

      //   $scope.tableProducto = true;

      //   if($scope.producto != undefined) {
      //     InventarioService.productos().then(function (data) {
      //       $scope.productos = data.filter(function (registro) {
      //         return $filter('lowercase')(registro.descripcion
      //                             .substring(0,$scope.producto.length)) == $filter('lowercase')($scope.producto);
      //       });

      //       if($scope.productos.length > 0){
      //         $scope.tableProducto = true;
      //         $scope.productoNoExiste = '';
      //       } else {
      //         $scope.tableProducto = false;
      //         $scope.productoNoExiste = 'No existe el producto'
      //       }

      //     });
      //   } else {
      //     InventarioService.productos().then(function (data) {
      //       $scope.productos = data;
      //     });
      //   }
      // }

      // //Traer productos
      // $scope.getSocio = function($event) {
      //   $event.preventDefault();

      //   $scope.tableSocio = true;

      //   if($scope.socioNombre != undefined) {
      //     FacturacionService.socios().then(function (data) {
      //       $scope.socios = data.filter(function (registro) {
      //         return $filter('lowercase')(registro.nombreCompleto
      //                             .substring(0,$scope.socioNombre.length)) == $filter('lowercase')($scope.socioNombre);
      //       });

      //       if($scope.socios.length > 0){
      //         $scope.tableSocio = true;
      //         $scope.socioNoExiste = '';
      //       } else {
      //         $scope.tableSocio = false;
      //         $scope.socioNoExiste = 'No existe el socio';
      //       }

      //     });
      //   } else {
      //     FacturacionService.socios().then(function (data) {
      //       $scope.socios = data;
      //       $scope.socioCodigo = '';
      //     });
      //   }
      // }

      // //Agregar Producto
      // $scope.addProducto = function($event, Prod) {
      //   $event.preventDefault();

      //   Prod.descuento = 0;
      //   Prod.cantidad = 1;
      //   $scope.dataD.push(Prod);
      //   $scope.tableProducto = false;

      //   $scope.calculaTotales();
      // }

      // //Seleccionar Socio
      // $scope.selSocio = function($event, s) {
      //   $event.preventDefault();

      //   $scope.socioNombre = s.nombreCompleto;
      //   $scope.socioCodigo = s.codigo;
      //   $scope.tableSocio = false;
      // }


      // // Calcula los totales para los productos
      // $scope.calculaTotales = function() {
      //   try {
      //     var total = 0;
      //     var subtotal = 0;
      //     var total_descuento = 0;
      //     var descuento = 0;

      //     $scope.dataD.forEach(function (item) {
      //       if (item.descuento != undefined && item.descuento > 0) {

      //         descuento = (item.descuento/100);
      //         descuento = item.precio * descuento * item.cantidad;
      //       }
      //       subtotal += (item.cantidad * item.precio);
      //       total = subtotal - descuento;
      //       total_descuento += descuento;

      //     });

      //     $scope.subtotal = $filter('number')(subtotal, 2);
      //     $scope.total = $filter('number')(total, 2);
      //     $scope.descuento = $filter('number')(total_descuento, 2);

      //   } catch (e) {
      //     $rootScope.mostrarError(e);

      //   }  
      // }


    }]);

})(_);