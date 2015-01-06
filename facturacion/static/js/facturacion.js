(function () {

  angular.module('cooperativa.facturacion', ['ngAnimate'])

    .factory('FacturacionService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Factura
      function guardarF(dataH, dataD) {
        var deferred = $q.defer();

        $http.post('/inventario/', JSON.stringify({'cabecera': dataH, 'detalle': dataD, 'almacen': almacen})).
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
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Buscar un documento en especifico (Desglose)
      // function DocumentoById(NoDoc) {
      //   var deferred = $q.defer();

      //   var doc = NoDoc != undefined? NoDoc : 0;

      //   $http.get('/inventariojson/?nodoc={NoDoc}&format=json'.replace('{NoDoc}', doc))
      //     .success(function (data) {
      //       deferred.resolve(data);
      //     });

      //   return deferred.promise;
      // }



      // //Listado de productos
      // function productos() {
      //   var deferred = $q.defer();

      //   $http.get('/api/producto/?format=json')
      //     .success(function (data) {
      //       deferred.resolve(data);
      //     });

      //   return deferred.promise;
      // }


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
        byNoFact: byNoFact
        // suplidores: suplidores,
        // productos: productos,
        // guardarEI: guardarEI,
        // DocumentoById: DocumentoById
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('ListadoFacturasCtrl', ['$scope', '$filter', 'FacturacionService', 'InventarioService', 
                                        function ($scope, $filter, FacturacionService, InventarioService) {
      $scope.errorShow = false;
      $scope.showLF = true;
      $scope.regAll = false;
      $scope.tableProducto = false;

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
        // $scope.producto = '';
        $scope.almacen = '';
        $scope.subtotal = '';
        $scope.total = '';
        
        $scope.dataH = {};
        $scope.dataD = [];
        $scope.productos = [];

        $scope.showLF = false;
        $scope.ArrowLF = 'DownArrow';
        $scope.dataH.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
        $scope.dataH.vendedor = usuario;
        $scope.dataH.terminos = 'CO';

        $scope.disabledButton = 'Boton';

      }


      //Traer productos
      $scope.getProducto = function($event) {
        $event.preventDefault();

        $scope.tableProducto = true;

        console.log($scope.producto);
        console.log(typeof($scope.producto));
        console.log($scope.xxp);

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

      //Agregar Producto
      $scope.addProducto = function($event, Prod) {
        $event.preventDefault();

        $scope.dataD.push(Prod);
        $scope.tableProducto = false;
      }

    }]);

})();