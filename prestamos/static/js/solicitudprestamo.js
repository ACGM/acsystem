(function (_) {

  angular.module('cooperativa.solicitudprestamo', ['ngAnimate'])

    .factory('SolicitudPrestamoService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      // //Guardar Desembolso Caja
      // function guardaDesembolso(dataH, dataD) {
      //   var deferred = $q.defer();

      //   $http.post('/desembolso/', JSON.stringify({'cabecera': dataH, 'detalle': dataD})).
      //     success(function (data) {
      //       deferred.resolve(data);
      //     }).
      //     error(function (data) {
      //       deferred.resolve(data);
      //     });

      //   return deferred.promise;
      // }

      //Llenar el listado de Solicitudes
      function solicitudesprestamos(noSolicitud) {
        var deferred = $q.defer();
        var url = "/api/prestamos/solicitudes/prestamos/?format=json";

        if (noSolicitud != undefined) {
            url = "/api/prestamos/solicitudes/prestamos/noSolicitud/?format=json".replace('noSolicitud', noSolicitud);
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Filtrar el listado de Solicitudes por Socio
      function solicitudesprestamosBySocio(dato) {
        var deferred = $q.defer();
        var url = "";

        if(!isNaN(dato)) {
          url = "/api/prestamos/solicitudes/prestamos/codigo/dato/".replace("dato", dato);
        } else {
          url = "/api/prestamos/solicitudes/prestamos/nombre/dato/".replace("dato", dato);
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Filtrar el listado de Solicitudes por estatus
      function solicitudesprestamosByEstatus(estatus) {
        var deferred = $q.defer();

        solicitudesprestamos(undefined).then(function (data) {
          var results = data.filter(function (registros) {
            if(estatus == 'T') {
              return registros;
            } else {
              return registros.estatus == estatus;
            }
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
        solicitudesprestamos: solicitudesprestamos,
        solicitudesprestamosBySocio: solicitudesprestamosBySocio,
        solicitudesprestamosByEstatus: solicitudesprestamosByEstatus
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('SolicitudPrestamoCtrl', ['$scope', '$filter', 'SolicitudPrestamoService', 
                                        function ($scope, $filter, SolicitudPrestamoService) {
      
      //Inicializacion de variables
      $scope.showLSP = true;
      $scope.regAll = false;
      $scope.estatus = 'T';


      $scope.item = {};
      $scope.solicitudes = {};

      $scope.solicitudesSeleccionadas = [];
      $scope.reg = [];
      $scope.valoresChk = [];

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLD = 'UpArrow';

      
      // Mostrar/Ocultar panel de Listado de Desembolsos
      $scope.toggleLSP = function() {
        $scope.showLSP = !$scope.showLSP;

        if($scope.showLSP === true) {
          $scope.ArrowLSP = 'UpArrow';
        } else {
          $scope.ArrowLSP = 'DownArrow';
        }
      }

      //Listado de todas las solicitudes de prestamos
      $scope.listadoSolicitudes = function(noSolicitud) {
        $scope.solicitudesSeleccionadas = [];
        $scope.valoresChk = [];
        $scope.estatus = 'T';

        SolicitudPrestamoService.solicitudesprestamos(noSolicitud).then(function (data) {
          $scope.solicitudes = data;
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

      $scope.solicitudesprestamosBySocio = function($event, socio) {

        if($event.keyCode == 13) {

          SolicitudPrestamoService.solicitudesprestamosBySocio(socio).then(function (data) {

            if(data.length > 0) {
              $scope.solicitudes = data;
              $scope.verTodos = '';
              $scope.NoFoundDoc = '';
            } else {
              $scope.NoFoundDoc = 'No se encontró el socio : ' + socio;
            }

          },
            function() {
              $scope.NoFoundDoc = 'No se encontró el socio : ' + socio;

            }
          );
        }
      }

      $scope.solicitudesprestamosEstatus = function(estatus) {

        SolicitudPrestamoService.solicitudesprestamosByEstatus(estatus).then(function (data) {
          $scope.solicitudes = data;

          if(data.length > 0) {
            $scope.verTodos = '';
            $scope.NoFoundDoc = '';
          }
        },
          function() {
            $scope.NoFoundDoc = "No existen solicitudes con el estatus : " + estatus;
          }
        );
      }

      //Cuando se le de click al checkbox del header.
      $scope.seleccionAll = function() {

        $scope.solicitudes.forEach(function (data) {
          if (data.estatus != 'A' && data.estatus != 'R' && data.estatus != 'C') {
            if ($scope.regAll === true){

              $scope.valoresChk[data.id] = true;
              $scope.solicitudesSeleccionadas.push(data);
            }
            else{

              $scope.valoresChk[data.id] = false;
              $scope.solicitudesSeleccionadas.splice(data);
            }
          }
        });
      }

      //Cuando se le de click a un checkbox de la lista
      $scope.selectedReg = function(iReg) {
        
        index = $scope.solicitudes.indexOf(iReg);

        if ($scope.reg[$scope.solicitudes[index].id] === true){
          $scope.solicitudesSeleccionadas.push($scope.solicitudes[index]);
        }
        else{

          $scope.solicitudesSeleccionadas.splice($scope.solicitudesSeleccionadas[index],1);
        }
      }

      //Nueva Entrada de Factura
      $scope.nuevaEntrada = function(usuario) {
        $scope.producto = '';
        $scope.almacen = '';
        $scope.subtotal = '';
        $scope.descuento = '';
        $scope.total = '';

        $scope.socioCodigo = '';
        $scope.socioNombre = '';
        
        $scope.dataH = {};
        $scope.dataD = [];
        $scope.productos = [];

        $rootScope.mostrarOrden(false);
        $scope.showLF = false;
        $scope.ArrowLF = 'DownArrow';
        $scope.BotonOrden = '';
        $scope.dataH.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
        $scope.dataH.vendedor = usuario;
        $scope.dataH.terminos = 'CO';
        $scope.dataH.posteo = 'N';

        $scope.disabledButton = 'Boton';
        $scope.disabledButtonBool = false;

      }



      // //Buscar un cheque en especifico
      // $scope.filtrarPorNoCheque = function(NoCheque) {
      //   try {
      //     FondosCajasService.byNoCheque(NoCheque).then(function (data) {
      //       $scope.desembolsos = data;

      //       if(data.length > 0) {
      //         $scope.verTodos = '';
      //         $scope.NoFoundDoc = '';
      //       }
      //     }, 
      //       (function () {
      //         $scope.NoFoundDoc = 'No se encontró el cheque #' + NoCheque;
      //       }
      //     ));          
      //   } catch (e) {
      //     console.log(e);
      //   }
      // }

      // //Buscar Cheque por ENTER
      // $scope.buscarCheque = function($event, NoCheque) {
      //   if($event.keyCode == 13) {
      //     $scope.filtrarPorNoCheque(NoCheque);
      //   }
      // }

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



      // // Mostrar/Ocultar error
      // $scope.toggleError = function() {
      //   $scope.errorShow = !$scope.errorShow;
      // }

      // // Funcion para mostrar error por pantalla
      // $rootScope.mostrarError = function(error) {
      //   $scope.errorMsg = error;
      //   $scope.errorShow = true;
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