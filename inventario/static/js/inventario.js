(function (_) {

  angular.module('cooperativa.inventario',['ngAnimate'])

    .filter('posteo', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('N', false)
                .replace('S', true);
        return input;
      }
    })    


    .factory('InventarioService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Entrada Inventario
      function guardarEI(dataH, dataD, almacen) {
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

      //Llenar el listado de entradas de inventario
      function all() {
        var deferred = $q.defer();

        $http.get('/api/inventario/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Listado de suplidores
      function suplidores() {
        var deferred = $q.defer();

        $http.get('/api/suplidor/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Listado de almacenes
      function almacenes() {
        var deferred = $q.defer();

        $http.get('/api/almacenes/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Listado de productos
      function productos() {
        var deferred = $q.defer();

        $http.get('/api/producto/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Buscar un numero de documento en especifico.
      function byNoDoc(NoDoc) {
        var deferred = $q.defer();
        all().then(function (data) {
          var result = data.filter(function (documento) {
            return documento.id == NoDoc;
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
        byNoDoc: byNoDoc,
        suplidores: suplidores,
        productos: productos,
        guardarEI: guardarEI,
        almacenes: almacenes
      };

    }])




    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('ListadoEntradaInvCtrl', ['$scope','$http', '$filter', 'InventarioService', function ($scope, $http, $filter, InventarioService) {
      $scope.errorShow = false;
      $scope.showLEI = true;
      $scope.regAll = false;
      $scope.tableProducto = false;

      $scope.item = {};
      $scope.entradas = {};

      $scope.entradasSeleccionadas = [];
      $scope.reg = [];
      $scope.valoresChk = [];
      $scope.dataD = [];

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLEI = 'UpArrow';

      
      //Guardar Entrada Inventario
      $scope.guardarEI = function() {
        try {

          var fechaP = $scope.dataH.fecha.split('/');
          var fechaFormatted = fechaP[2] + '-' + fechaP[1] + '-' + fechaP[0];

          if ($scope.dataH.fechaVence != undefined) {
            var fechaVP = $scope.dataH.fechaVence.split('/');
            var fechaVFormatted = fechaVP[2] + '-' + fechaVP[1] + '-' + fechaVP[0];  
          }
          
          
          var dataH = new Object();

          dataH.suplidor = $scope.dataH.idSuplidor;
          dataH.factura = $scope.dataH.factura != undefined? $scope.dataH.factura : '';
          dataH.orden = $scope.dataH.ordenNo != undefined? $scope.dataH.ordenNo : '';
          dataH.ncf = $scope.dataH.ncf != undefined? $scope.dataH.ncf : '';
          dataH.fecha = fechaFormatted;
          dataH.condicion = $scope.dataH.condicion;
          dataH.diasPlazo = $scope.dataH.venceDias != undefined? $scope.dataH.venceDias : '';
          dataH.nota = $scope.dataH.nota != undefined? $scope.dataH.nota : '';
          dataH.vence = fechaVFormatted != undefined? fechaVFormatted: '';
          dataH.userlog = $scope.dataH.usuario;

          if ($scope.dataD.length == 0) {
            throw "Debe agregar un producto al menos.";
          }

          InventarioService.guardarEI(dataH,$scope.dataD,$scope.almacen).then(function (data) {
            if (data != '1') {
              throw data;
            } else {
              $scope.errorShow = false;
              $scope.listadoEntradas();

              $scope.toggleLEI();
              $scope.dataH = {};
              $scope.dataD = [];
              $scope.almacen = '';
              $scope.subtotal = '';
              $scope.total = '';
            }

          },
          (function () {
            $scope.errorMsg = 'Hubo un error. Contacte al administrador del sistema.';
            $scope.toggleError();
          }
          ));
        }

        catch (e) {
          console.log('ERROR:'+ e);
          $scope.errorMsg = e;
          $scope.errorShow = true;
        }
      }

      $scope.calculaTotales = function() {
        var total = 0;
        var subtotal = 0;

        $scope.dataD.forEach(function (item) {
          total += (item.cantidad * item.costo);
        });

        $scope.subtotal = $filter('number')(total, 2);
        $scope.total = $filter('number')(total, 2);
      }

      //Eliminar producto de la lista de entradas
      $scope.delProducto = function(prod) {
        index = $scope.dataD.indexOf(prod);
        console.log(index);

        $scope.dataD.splice($scope.dataD[index],1);
      }


      //Nueva Entrada de Inventario
      $scope.nuevaEntrada = function(usuario) {
        $scope.productos = [];
        $scope.showLEI = false;
        $scope.ArrowLEI = 'DownArrow';

        $scope.dataH = {};
        $scope.dataH.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

        $scope.focusSuplidor = true;
        $scope.dataH.usuario = usuario;
      }


      //Calcula Fecha Vence
      $scope.venceFecha = function() {
        var fechaP = $scope.dataH.fecha.split('/');
        var fechaF = new Date(fechaP[2] + '/' + fechaP[1] + '/' + fechaP[0]);

        if ($scope.dataH.venceDias != undefined && fechaF != 'Invalid Date') {
          var nextDate = new Date();
          nextDate.setDate(fechaF.getDate()+parseInt($scope.dataH.venceDias));

          $scope.dataH.fechaVence = $filter('date')(nextDate, 'dd/MM/yyyy');
        } else {
          $scope.dataH.fechaVence = '';
        }
      }


      //Traer suplidores
      $scope.getSuplidor = function(suplidor) {
        if(suplidor != undefined) {
          InventarioService.suplidores().then(function (data) {
            $scope.suplidores = data.filter(function (registro) {
              return registro.id == suplidor;
            });

            if($scope.suplidores.length > 0) {
              $scope.dataH.suplidorNombre = $scope.suplidores[0].nombre;
            }

          });
        } else {
          InventarioService.suplidores().then(function (data) {
            $scope.suplidores = data;

          });
        }
      }


      //Traer almacenes
      $scope.getAlmacenes = function() {
        InventarioService.almacenes().then(function (data) {
          $scope.almacenes = data;
        });
      }


      //Traer productos
      $scope.getProducto = function($event) {
        $event.preventDefault();

        $scope.tableProducto = true;

        if($scope.producto != undefined) {

          InventarioService.productos().then(function (data) {

            $scope.productos = data.filter(function (registro) {
              return $filter('lowercase')(registro.descripcion.substring(0,$scope.producto.length)) == $filter('lowercase')($scope.producto);
            });

            if($scope.productos.length > 0){
              $scope.tableProducto = true;
              $scope.productoNoExiste = '';
            } else {
              $scope.tableProducto = false;
              $scope.productoNoExiste = 'No existe el producto'
            }

          });
        } 
        else {
          InventarioService.productos().then(function (data) {
            $scope.productos = data;

          });
        }

      }


      //Agregar Producto
      $scope.addProducto = function($event,Prod) {
        $event.preventDefault();

        index = $scope.productos.indexOf(Prod);
        $scope.dataD.push(Prod);
        $scope.tableProducto = false;
      }

      
      //Listado de todas las entradas de inventario
      $scope.listadoEntradas = function() {
        $scope.entradasSeleccionadas = [];
        $scope.valoresChk = [];
        $scope.regAll = false;

        InventarioService.all().then(function (data) {
          $scope.entradas = data.reverse();

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


      //Buscar una entrada de inventario en especifico
      $scope.filtrarPorNoDoc = function(NoDoc) {
        InventarioService.byNoDoc(NoDoc).then(function (data) {
          $scope.entradas = data;

          if(data.length > 0) {
            $scope.verTodos = '';
            $scope.NoFoundDoc = '';
          }
        }, 
          (function () {
            $scope.NoFoundDoc = 'No se encontró el documento #' + NoDoc;
          }
        ));

      }


      //Buscar Documento por ENTER
      $scope.buscarDoc = function($event, NoDoc) {
        if($event.keyCode == 13) {
          $scope.filtrarPorNoDoc(NoDoc);
        }
      }

      //Filtrar las entradas de inventario por posteo (SI/NO)
      $scope.filtrarPosteo = function() {
        $scope.entradasSeleccionadas = [];
        $scope.valoresChk = [];
        $scope.regAll = false;

        if($scope.posteof != '*') {
          InventarioService.byPosteo($scope.posteof).then(function (data) {
            $scope.entradas = data.reverse();

            if(data.length > 0){
              $scope.verTodos = '';
            }
        });
        } else {
          $scope.listadoEntradas();

        }        
      }


      //Visualizar Documento (Entrada de Inventario Existente - desglose)
      $scope.visualizarDoc = function(NoDoc) {
        InventarioService.byNoDoc(NoDoc).then(function (data) {
          $scope.DocView = data[0];

          // dataH.diasPlazo = $scope.venceDias;
          // dataH.nota = $scope.nota;
          // dataH.vence = '2014-12-30';
          // dataH.userlog = 'coop';

          // $scope.idSuplidor = $scope.DocView.suplidor;
          $scope.factura = $scope.DocView.factura;
          // $scope.ordenNo = $scope.DocView.orden;
          // $scope.ncf = $scope.DocView.ncf;
          // $scope.fecha = $scope.DocView.fecha;
          // $scope.condicion = $scope.DocView.condicion;
          // $scope.diasPlazo = $scope.DocView.diasPlazo;
          $scope.toggleLEI();
        });
      }


      // Mostrar/Ocultar panel de Listado de Entrada Inventario
      $scope.toggleLEI = function() {
        $scope.showLEI = !$scope.showLEI;

        if($scope.showLEI === true) {
          $scope.ArrowLEI = 'UpArrow';
        } else {
          $scope.ArrowLEI = 'DownArrow';
        }
      }

      // Mostrar/Ocultar error
      $scope.toggleError = function() {
        $scope.errorShow = !$scope.errorShow;
      }


      //Cuando se le de click al checkbox del header.
      $scope.seleccionAll = function() {

        $scope.entradas.forEach(function (data) {
          if (data.posteo == 'N') {
            if ($scope.regAll === true){

              $scope.valoresChk[data.id] = true;
              $scope.entradasSeleccionadas.push(data);
            }
            else{

              $scope.valoresChk[data.id] = false;
              $scope.entradasSeleccionadas.splice(data);
            }
          }

        });
      }

      
      //Cuando se le de click a un checkbox de la lista
      $scope.selectedReg = function(iReg) {
        
        index = $scope.entradas.indexOf(iReg);

        if ($scope.reg[$scope.entradas[index].id] === true){
          $scope.entradasSeleccionadas.push($scope.entradas[index]);
        }
        else{
          $scope.entradasSeleccionadas.splice($scope.entradasSeleccionadas[index],1);
        }
      }


      $scope.postear = function(){

      }

    }])



    .controller('EntradaInvCtrl', ['$scope', function ($scope) {
      $scope.showEI = true;

      // Mostrar/Ocultar panel de Entrada de Inventario
      $scope.toggleEI = function() {
        $scope.showEI = !$scope.showEI;
      }

    }]);

})(_);  