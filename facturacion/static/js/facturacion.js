(function (_) {

  angular.module('cooperativa.facturacion', ['ngAnimate'])

    .factory('FacturacionService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Factura
      function guardarFact(dataH, dataD) {
        var deferred = $q.defer();

        $http.post('/facturacion/', JSON.stringify({'cabecera': dataH, 'detalle': dataD})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Guardar Orden de Compra
      function guardarOrdenSC(Orden) {
        var deferred = $q.defer();
        $http.post('/ordenSuperCoop/', JSON.stringify({'orden': Orden})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Llenar el listado de facturas
      function all() {
        var deferred = $q.defer();

        $http.get('/api/facturas/?format=json')
          .success(function (data) {
            deferred.resolve(data.filter( function(item) {
              return item.posteo == "N" || item.posteo == "S";

            }));
          });

        return deferred.promise;
      }

      //Categorias de prestamos, si se pasa el parametro "cp" con valor es filtrada la informacion. 
      function categoriasPrestamos(cp) {
        var deferred = $q.defer();

        $http.get('/api/categoriasPrestamos/?format=json')
          .success(function (data) {
            if (cp != undefined) {
              deferred.resolve(data.filter( function(item) {
                return item.descripcion == cp;

              }));
            } else {
              deferred.resolve(data);
            }
          });

        return deferred.promise;
      }

      //Traer el listado de socios
      function socios() {
        var deferred = $q.defer();

        $http.get('/api/socio/?format=json')
          .success(function (data) {
            deferred.resolve(data.filter( function(socio) {
              return socio.estatus == "E" || socio.estatus == "S";

            }));
          });

        return deferred.promise;
      }


      //Buscar un documento en especifico (Desglose)
      function DocumentoById(NoFact) {
        var deferred = $q.defer();
        var doc = NoFact != undefined? NoFact : 0;

        $http.get('/facturajson/?nofact={NoFact}&format=json'.replace('{NoFact}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Buscar un numero de documento en especifico en listado de documentos
      function byNoFact(NoFact) {
        var deferred = $q.defer();
        all().then(function (data) {
          var result = data.filter(function (documento) {
            return documento.noFactura == NoFact;
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
            return registros.posteo == valor;
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
        byNoFact: byNoFact,
        socios: socios,
        guardarFact: guardarFact,
        DocumentoById: DocumentoById,
        categoriasPrestamos: categoriasPrestamos,
        guardarOrdenSC: guardarOrdenSC
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('ListadoFacturasCtrl', ['$scope', '$filter', '$rootScope', '$timeout', 'FacturacionService', 'InventarioService', 
                                        function ($scope, $filter, $rootScope, $timeout, FacturacionService, InventarioService) {
      
      //Inicializacion de variables
      $rootScope.mostrarOC = false;
      $scope.disabledButton = 'Boton-disabled';
      $scope.disabledButtonBool = true;
      $scope.posteof = '*';
      $scope.errorShow = false;
      $scope.showLF = true;
      $scope.regAll = false;
      $scope.tableProducto = false;
      $scope.tableSocio = false;

      $scope.item = {};
      $scope.facturas = {};

      $scope.facturasSeleccionadas = [];
      $scope.reg = [];
      $scope.valoresChk = [];
      $scope.dataD = [];

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLF = 'UpArrow';

      
      // Mostrar/Ocultar panel de Listado de Facturas
      $scope.toggleLF = function() {
        $scope.showLF = !$scope.showLF;

        if($scope.showLF === true) {
          $scope.ArrowLF = 'UpArrow';
        } else {
          $scope.ArrowLF = 'DownArrow';
        }
      }


      //Listado de todas las facturas
      $scope.listadoFacturas = function() {
        $scope.NoFoundDoc = '';
        $scope.facturasSeleccionadas = [];
        $scope.valoresChk = [];

        FacturacionService.all().then(function (data) {
          $scope.facturas = data;
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

      //Guardar Factura
      $scope.guardarFactura = function($event) {
        $event.preventDefault();

        try {
          if (!$scope.FacturaForm.$valid) {
            throw "Verifique que todos los campos esten completados correctamente.";
          }

          var fechaP = $scope.dataH.fecha.split('/');
          var fechaFormatted = fechaP[2] + '-' + fechaP[1] + '-' + fechaP[0];

          var dataH = new Object();

          dataH.factura = $scope.dataH.factura != undefined? $scope.dataH.factura : 0;
          dataH.fecha = fechaFormatted;
          dataH.terminos = $scope.dataH.terminos;
          dataH.vendedor = $scope.dataH.vendedor;
          dataH.almacen = $scope.dataH.almacen;
          dataH.socio = $scope.socioCodigo != undefined? $scope.socioCodigo : null;
          dataH.orden = $scope.orden != undefined? $scope.orden : null;

          if ($scope.dataD.length == 0) {
            throw "Debe agregar un producto al menos.";
          }

          FacturacionService.guardarFact(dataH,$scope.dataD).then(function (data) {
            if(data.substring(0,2) == 'NO') {
              $rootScope.mostrarError(data);
              throw data;
            }

            $rootScope.factura = data;
            $scope.dataH.factura = $filter('numberFixedLen')(data, 8)

            $scope.errorShow = false;
            $scope.listadoFacturas();

            //SI ES A CREDITO LA FACTURA SE DEBE CREAR UNA ORDEN DE DESPACHO SUPERRCOOP
            if($scope.dataH.terminos == "CR") {

              $scope.mostrarOrden(true);
              $scope.disabledButton = 'Boton-disabled';
              $scope.disabledButtonBool = true;
              $scope.BotonOrden = 'BotonOrden';

              $rootScope.total = $scope.total;
              $rootScope.getCategoriaPrestamo($scope.dataH.vendedor);

              if ($rootScope.oid > 0) {
                $rootScope.guardarOrden($event);
              }

              } else {              
                $scope.nuevaEntrada();
                $scope.toggleLF();
              }
          },
          (function () {
            $rootScope.mostrarError('Hubo un error. Contacte al administrador del sistema.');
          }
          ));

        }
        catch (e) {
          $rootScope.mostrarError(e);
        }
      }

      // Visualizar Documento (Factura Existente - desglose)
      $scope.FactFullById = function(NoFact, usuario) {
        try {
          FacturacionService.DocumentoById(NoFact).then(function (data) {

            if(data.length > 0) {
              $scope.errorMsg = '';
              $scope.errorShow = false;

              //completar los campos
              $scope.nuevaEntrada();

              $scope.dataH.factura = $filter('numberFixedLen')(NoFact, 8);
              $scope.dataH.fecha = $filter('date')(data[0]['fecha'], 'dd/MM/yyyy');
              $scope.socioCodigo = data[0]['socioCodigo'];
              $scope.socioNombre = data[0]['socioNombre'];
              $scope.dataH.orden = $filter('numberFixedLen')(data[0]['orden'], 8);
              $scope.dataH.terminos = data[0]['terminos'];
              $scope.dataH.vendedor = data[0]['vendedor'];
              $scope.dataH.posteo = data[0]['posteo'];

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

        $scope.toggleLF();
      }


      //Eliminar producto de la lista de entradas
      $scope.delProducto = function($event, prod) {
        $event.preventDefault();
        try {
          $scope.dataD = _.without($scope.dataD, _.findWhere($scope.dataD, {codigo: prod.codigo}));

          $scope.calculaTotales();
          
        } catch (e) {
          $rootScope.mostrarError(e);
        }
      }

      //Traer almacenes
      $scope.getAlmacenes = function() {
        InventarioService.almacenes().then(function (data) {
          $scope.almacenes = data;
        });
      }

      //Filtrar las facturas por posteo (SI/NO)
      $scope.filtrarPosteo = function() {
        $scope.facturasSeleccionadas = [];
        $scope.valoresChk = [];
        $scope.regAll = false;

        if($scope.posteof != '*') {
          FacturacionService.byPosteo($scope.posteof).then(function (data) {
            $scope.facturas = data;

            if(data.length > 0){
              $scope.verTodos = '';
            }
        });
        } else {
          $scope.listadoFacturas();
        }        
      }

       //Buscar una factura en especifico
      $scope.filtrarPorNoFact = function(NoFact) {
        try {
          FacturacionService.byNoFact(NoFact).then(function (data) {
            $scope.facturas = data;

            if(data.length > 0) {
              $scope.verTodos = '';
              $scope.NoFoundDoc = '';
            }
          }, 
            (function () {
              $scope.NoFoundDoc = 'No se encontró el documento #' + NoFact;
            }
          ));          
        } catch (e) {
          console.log(e);
        }
      }

      //Buscar Documento por ENTER
      $scope.buscarFact = function($event, NoFact) {
        if($event.keyCode == 13) {
          $scope.filtrarPorNoFact(NoFact);
        }
      }

      // Mostrar/Ocultar error
      $scope.toggleError = function() {
        $scope.errorShow = !$scope.errorShow;
      }

      // Funcion para mostrar error por pantalla
      $rootScope.mostrarError = function(error) {
        $scope.errorMsg = error;
        $scope.errorShow = true;

        // $timeout($scope.toggleError(), 3000);
        
      }

      //Cuando se le de click al checkbox del header.
      $scope.seleccionAll = function() {

        $scope.facturas.forEach(function (data) {
          if (data.posteo == 'N') {
            if ($scope.regAll === true){

              $scope.valoresChk[data.id] = true;
              $scope.facturasSeleccionadas.push(data);
            }
            else{

              $scope.valoresChk[data.id] = false;
              $scope.facturasSeleccionadas.splice(data);
            }
          }

        });
      }

      
      //Cuando se le de click a un checkbox de la lista
      $scope.selectedReg = function(iReg) {
        
        index = $scope.facturas.indexOf(iReg);

        if ($scope.reg[$scope.facturas[index].id] === true){
          $scope.facturasSeleccionadas.push($scope.facturas[index]);
        }
        else{

          $scope.facturasSeleccionadas.splice($scope.facturasSeleccionadas[index],1);
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

        $rootScope.clearOrden();
      }


      //Traer productos
      $scope.getProducto = function($event) {
        $event.preventDefault();

        $scope.tableProducto = true;

        if($scope.producto != undefined) {
          InventarioService.productos().then(function (data) {
            $scope.productos = data.filter(function (registro) {
              return $filter('lowercase')(registro.descripcion
                                  .substring(0,$scope.producto.length)) == $filter('lowercase')($scope.producto);
            });

            if($scope.productos.length > 0){
              $scope.tableProducto = true;
              $scope.productoNoExiste = '';
            } else {
              $scope.tableProducto = false;
              $scope.productoNoExiste = 'No existe el producto'
            }

          });
        } else {
          InventarioService.productos().then(function (data) {
            $scope.productos = data;
          });
        }
      }

      //Traer productos
      $scope.getSocio = function($event) {
        $event.preventDefault();

        $scope.tableSocio = true;

        if($scope.socioNombre != undefined) {
          FacturacionService.socios().then(function (data) {
            $scope.socios = data.filter(function (registro) {
              return $filter('lowercase')(registro.nombreCompleto
                                  .substring(0,$scope.socioNombre.length)) == $filter('lowercase')($scope.socioNombre);
            });

            if($scope.socios.length > 0){
              $scope.tableSocio = true;
              $scope.socioNoExiste = '';
            } else {
              $scope.tableSocio = false;
              $scope.socioNoExiste = 'No existe el socio';
            }

          });
        } else {
          FacturacionService.socios().then(function (data) {
            $scope.socios = data;
            $scope.socioCodigo = '';
          });
        }
      }

      //Agregar Producto
      $scope.addProducto = function($event, Prod) {
        $event.preventDefault();

        Prod.descuento = 0;
        Prod.cantidad = 1;
        $scope.dataD.push(Prod);
        $scope.tableProducto = false;

        $scope.calculaTotales();
      }

      //Seleccionar Socio
      $scope.selSocio = function($event, s) {
        $event.preventDefault();

        $scope.socioNombre = s.nombreCompleto;
        $scope.socioCodigo = s.codigo;
        $scope.tableSocio = false;
      }


      // Calcula los totales para los productos
      $scope.calculaTotales = function() {
        try {
          var total = 0;
          var subtotal = 0;
          var total_descuento = 0;
          var descuento = 0;

          $scope.dataD.forEach(function (item) {
            if (item.descuento != undefined && item.descuento > 0) {

              descuento = (item.descuento/100);
              descuento = item.precio * descuento * item.cantidad;
            }
            subtotal += (item.cantidad * item.precio);
            total = subtotal - descuento;
            total_descuento += descuento;

          });

          $scope.subtotal = $filter('number')(subtotal, 2);
          $scope.total = $filter('number')(total, 2);
          $scope.descuento = $filter('number')(total_descuento, 2);

        } catch (e) {
          $rootScope.mostrarError(e);

        }  
      }


    }])

   .controller('OrdenSuperCoopCtrl', ['$scope', '$filter', '$rootScope', 'FacturacionService',
                                      function ($scope, $filter, $rootScope, FacturacionService) {
    
      //Inicializacion de variables
      // Limpiar Orden de Compra
      $rootScope.clearOrden = function() {
        $scope.OC = {};
        $scope.disableOC = false;
        $scope.BotonOC = 'Boton';
      }
      $rootScope.oid = 0;
      $scope.showOC = false;
      $rootScope.clearOrden();


      // Mostrar/Ocultar panel para llenar datos de orden de compra
      $rootScope.mostrarOrden = function(valor) {
        $scope.showOC = valor;
        
      }

      //Traer datos de Categoria de Prestamo SUPERCOOP.
      $rootScope.getCategoriaPrestamo = function(oficial) {
        FacturacionService.categoriasPrestamos("SUPERCOOP").then(function (data) {

          $scope.OC.oficial = oficial;
          $scope.OC.categoriaId = data[0]['id'];
          $scope.OC.categoriaDescrp = data[0]['descripcion'];
          $scope.OC.interesA = data[0]['interesAnualSocio'];
          $scope.OC.interesM = parseFloat(data[0]['interesAnualSocio'])/12;
          $scope.OC.pagarPor = 'EM';
          $scope.OC.formaPago = 'Q';
          $scope.OC.quincena = '1';
          $scope.OC.cantidadCuotas = 2;
          $scope.OC.valorCuotas = $filter('number')(parseFloat($rootScope.total.replace(',','')) /2, 2);

        });
      }

      //Guardar Orden de Compra SUPERCOOP
      $rootScope.guardarOrden = function($event) {
        $event.preventDefault();

        try {
          var Orden = new Object();
          Orden.solicitud = $scope.OC.solicitud != undefined? parseInt('0' + $scope.OC.solicitud) : 0;
          Orden.categoriaPrestamo = $scope.OC.categoriaId;
          Orden.oficial = $scope.OC.oficial;
          Orden.pagarPor = $scope.OC.pagarPor;
          Orden.formaPago = $scope.OC.formaPago;
          Orden.tasaInteresAnual = $scope.OC.interesA;
          Orden.tasaInteresMensual = $scope.OC.interesA / 12;
          Orden.quincena = $scope.OC.quincena;
          Orden.cantidadCuotas = $scope.OC.cantidadCuotas;
          Orden.valorCuotas = $filter('number')(parseFloat($rootScope.total.replace(',','')) /2, 2).replace(',',''); //$scope.OC.valorCuotas.replace(',','');
          Orden.factura = $rootScope.factura;

          FacturacionService.guardarOrdenSC(Orden).then(function (data) {
            if(angular.isNumber(parseInt(data))) {
              $scope.OC.solicitud = $filter('numberFixedLen')(data, 8)
              
              $scope.disableOC = true;
              $scope.BotonOC = 'Boton-disabled';

            } else {
              throw data;
            }

          },
          (function () {
            $rootScope.mostrarError('Hubo un error. Contacte al administrador del sistema.');
          }
          ));

        }
        catch (e) {
          $rootScope.mostrarError(e);
        }
      }

      $rootScope.FullOrden = function(ordenD) {
        try {
          $scope.showOC = true;
          $scope.disableOC = true;
          $scope.BotonOC = 'Boton-disabled';

          $scope.OC.solicitud = $filter('numberFixedLen')(ordenD['solicitud'], 8);
          $scope.OC.categoriaId = ordenD['categoriaId'];
          $scope.OC.categoriaDescrp = ordenD['categoriaDescrp'];
          $scope.OC.oficial = ordenD['oficial'];
          $scope.OC.pagarPor = ordenD['pagarPor'];
          $scope.OC.formaPago = ordenD['formaPago'];
          $scope.OC.quincena = ordenD['quincena'];
          $scope.OC.interesA = ordenD['tasaInteresAnual'];
          $scope.OC.interesM = ordenD['tasaInteresMensual']
          $scope.OC.cantidadCuotas = ordenD['cuotas'];
          $scope.OC.valorCuotas = $filter('number')(ordenD['valorCuotas'], 2);

          $rootScope.oid = $scope.OC.solicitud;

        } catch (e) {
          $rootScope.mostrarError(e);
        }
      }

      
    }]);    
   

})(_);