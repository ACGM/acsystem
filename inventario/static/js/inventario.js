(function (_) {

  angular.module('cooperativa.inventario',['ngAnimate'])

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

      //Buscar un documento en especifico (Desglose)
      function DocumentoById(NoDoc) {
        var deferred = $q.defer();

        var doc = NoDoc != undefined? NoDoc : 0;

        $http.get('/inventariojson/?nodoc={NoDoc}&format=json'.replace('{NoDoc}', doc))
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

      //Buscar un numero de documento en especifico en listado de documentos
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
        almacenes: almacenes,
        DocumentoById: DocumentoById
      };

    }])




    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('ListadoEntradaInvCtrl', ['$scope', '$filter', 'InventarioService', function ($scope, $filter, InventarioService) {
      
      //Inicializacion de variables
      $scope.posteof = '*';
      $scope.errorShow = false;
      $scope.showLEI = true;
      $scope.regAll = false;
      $scope.tableProducto = false;

      $scope.item = {};
      $scope.entradas = {};
      $scope.dataH = {};

      $scope.entradasSeleccionadas = [];
      $scope.reg = [];
      $scope.valoresChk = [];
      $scope.dataD = [];

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLEI = 'UpArrow';

      
       //Listado de todas las entradas de inventario
      $scope.listadoEntradas = function() {
        $scope.NoFoundDoc = '';
        $scope.entradasSeleccionadas = [];
        $scope.valoresChk = [];
        $scope.regAll = false;

        InventarioService.all().then(function (data) {
          $scope.entradas = data;

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
        try {
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
        } catch (e) {
          $scope.mostrarError(e);
          console.log(e);
        }
      }

      //Buscar Documento por ENTER
      $scope.buscarDoc = function($event, NoDoc) {
        if($event.keyCode == 13) {
          $scope.filtrarPorNoDoc(NoDoc);
        }
      }

      //Filtrar las entradas de inventario por posteo (SI/NO)
      $scope.filtrarPosteo = function() {
        try {

          $scope.entradasSeleccionadas = [];
          $scope.valoresChk = [];
          $scope.regAll = false;

          if($scope.posteof != '*') {
            InventarioService.byPosteo($scope.posteof).then(function (data) {
              $scope.entradas = data;

              if(data.length > 0){
                $scope.verTodos = '';
              }
            });
          } else {
            $scope.listadoEntradas();

          }        
        } catch (e) {
          $scope.mostrarError(e);
        }
      }
        
      // Funcion para mostrar error por pantalla
      $scope.mostrarError = function(error) {
        $scope.errorMsg = error;
        $scope.errorShow = true;
      }

      //Guardar Entrada Inventario
      $scope.guardarEI = function() {
        try {
          if (!$scope.EntradaInventarioForm.$valid) {
            throw "Verifique que todos los campos esten completados correctamente.";
          }

          var fechaP = $scope.dataH.fecha.split('/');
          var fechaFormatted = fechaP[2] + '-' + fechaP[1] + '-' + fechaP[0];

          if ($scope.dataH.fechaVence != undefined) {
            var fechaVP = $scope.dataH.fechaVence.split('/');
            var fechaVFormatted = fechaVP[2] + '-' + fechaVP[1] + '-' + fechaVP[0];  
          }
          
          
          var dataH = new Object();

          dataH.suplidor = $scope.dataH.idSuplidor;
          dataH.entradaNo = $scope.dataH.entradaNo != undefined? $scope.dataH.entradaNo : 0;
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
              $scope.mostrarError(data);
              throw data;
            } else {
              $scope.errorShow = false;
              $scope.listadoEntradas();

              $scope.nuevaEntrada();
              $scope.toggleLEI();
            }

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

       // Visualizar Documento (Entrada de Inventario Existente - desglose)
      $scope.DocFullById = function(NoDoc) {
        try {
          InventarioService.DocumentoById(NoDoc).then(function (data) {

            if(data.length > 0) {
              $scope.errorMsg = '';
              $scope.errorShow = false;

              //completar los campos
              $scope.nuevaEntrada();

              $scope.dataH.entradaNo = $filter('numberFixedLen')(NoDoc, 8);
              $scope.dataH.idSuplidor = data[0]['suplidorId'];
              $scope.dataH.suplidorNombre = data[0]['suplidorName'];
              $scope.dataH.factura = data[0]['factura'];
              $scope.dataH.ordenNo = data[0]['orden'];
              $scope.dataH.ncf = data[0]['ncf'];
              $scope.dataH.fecha = $filter('date')(data[0]['fecha'],'dd/MM/yyyy');
              $scope.dataH.condicion = data[0]['condicion'];
              $scope.dataH.venceDias = data[0]['diasPlazo'];
              $scope.dataH.nota = data[0]['nota'];
              $scope.dataH.posteo = data[0]['posteo'];
              $scope.dataH.usuario = data[0]['usuario'];

              data[0]['productos'].forEach(function (item) {
                $scope.dataD.push(item);
                $scope.almacen = item['almacen'];
              })
              
              if (data[0]['diasPlazo'] != '') {
                $scope.venceFecha();
              }

              $scope.calculaTotales();
            }

          }, 
            (function () {
              $scope.mostrarError('No pudo encontrar el desglose del documento #' + NoDoc);
            }
          ));
        }
        catch (e) {
          $scope.mostrarError(e);
        }

        $scope.toggleLEI();

      }

      // Calcula los totales para los productos
      $scope.calculaTotales = function() {
        try {
          var total = 0;
          var subtotal = 0;

          $scope.dataD.forEach(function (item) {
            total += (item.cantidad * item.costo);
          });

          $scope.subtotal = $filter('number')(total, 2);
          $scope.total = $filter('number')(total, 2);

        } catch (e) {
          $scope.mostrarError(e);

        }
        
      }

      //Eliminar producto de la lista de entradas
      $scope.delProducto = function($event, prod) {
        $event.preventDefault();
        
        try {
          $scope.dataD = _.without($scope.dataD, _.findWhere($scope.dataD, {codigo: prod.codigo}));

          $scope.calculaTotales();
          
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Nueva Entrada de Inventario
      $scope.nuevaEntrada = function(usuario) {
        $scope.producto = '';
        $scope.almacen = '';
        $scope.subtotal = '';
        $scope.total = '';
        
        $scope.dataH = {};
        $scope.dataD = [];
        $scope.productos = [];

        $scope.showLEI = false;
        $scope.ArrowLEI = 'DownArrow';
        $scope.dataH.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
        $scope.dataH.usuario = usuario;
        $scope.dataH.condicion = 'CO';
        $scope.dataH.posteo = 'N';

        $scope.disabledButton = 'Boton';

      }

      //Calcula Fecha Vence
      $scope.venceFecha = function() {
        try {
          var fechaP = $scope.dataH.fecha.split('/');
          var fechaF = new Date(fechaP[2] + '/' + fechaP[1] + '/' + fechaP[0]);

          if ($scope.dataH.venceDias != undefined && fechaF != 'Invalid Date') {
            var nextDate = new Date();
            nextDate.setDate(fechaF.getDate()+parseInt($scope.dataH.venceDias));

            $scope.dataH.fechaVence = $filter('date')(nextDate, 'dd/MM/yyyy');
          } else {
            $scope.dataH.fechaVence = '';
          }
        } catch (e) {
          $scope.mostrarError(e);
        }
        
      }

      //Traer almacenes
      $scope.getAlmacenes = function() {
        InventarioService.almacenes().then(function (data) {
          $scope.almacenes = data;
        });
      }


      //Traer suplidores
      $scope.getSuplidor = function($event) {
        $event.preventDefault();

        $scope.tableSuplidor = true;

        
        if($scope.dataH.suplidorNombre != undefined) {
          InventarioService.suplidores().then(function (data) {
            $scope.suplidores = data.filter(function (registro) {
              return $filter('lowercase')(registro.nombre
                          .substring(0,$scope.dataH.suplidorNombre.length)) == $filter('lowercase')($scope.dataH.suplidorNombre);
            });

            if($scope.suplidores.length > 0) {
              $scope.tableSuplidor = true;
              $scope.suplidorNoExiste = '';
            } else {
              $scope.tableSuplidor = false;
              $scope.suplidorNoExiste = 'No existe el suplidor';
            }

          });
        } else {
          InventarioService.suplidores().then(function (data) {
            $scope.suplidores = data;
          });
        }
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


      //Seleccionar Suplidor
      $scope.selSuplidor = function($event, supl) {
        $event.preventDefault();

        $scope.dataH.idSuplidor = supl.id;
        $scope.dataH.suplidorNombre = supl.nombre;
        $scope.tableSuplidor = false;
      }

      //Agregar Producto
      $scope.addProducto = function($event, Prod) {
        $event.preventDefault();

        $scope.dataD.push(Prod);
        $scope.tableProducto = false;
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


      //Funcion para postear los registros seleccionados. (Postear es llevar al Diario)
      $scope.postear = function(){

      }

    }]);

})(_);  