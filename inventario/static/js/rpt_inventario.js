(function (_) {

  angular.module('cooperativa.inventarioRPT',['ngAnimate'])

    .factory('InventarioServiceRPT', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Llenar el listado de entradas de inventario
      function all() {
        var deferred = $q.defer();

        $http.get('/api/inventario/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Llenar el listado de categorias
      function categorias() {
        var deferred = $q.defer();

        $http.get('/api/categoriasProductos/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Existencia de Productos (filtros: Almacen, categorias)
      function existencia(almacen, categorias) {
        var deferred = $q.defer();
        var stringCategorias = "";

        if (almacen != '*') {
          if(categorias != undefined) {
            for(i=0; i<categorias.length; i++) {
              stringCategorias += categorias[i]['id'].toString() + ",";
            }
            // Si el almacen es uno en especifico y la(s) categoria(s) son especificadas.
            url = '/inventario/api/reportes/existencia/?format=json&almacen=@almacen&categorias=@categorias'.replace('@almacen', almacen).replace('@categorias',stringCategorias);
          } else {
            // Si el almacen es especificado y las categorias NO.
            url = '/inventario/api/reportes/existencia/?format=json&almacen=@almacen'.replace('@almacen',almacen);
          }
        } else {
          if(categorias != undefined) {
            for(i=0; i<categorias.length; i++) {
              stringCategorias += categorias[i]['id'].toString() + ",";
            }
            // Si NO es especificado ningun almacen pero SI las categorias.
            url = '/inventario/api/reportes/existencia/?format=json&categorias=@categorias'.replace('@categorias',stringCategorias);
          } else {
            // Si NO es especificado ningun almacen NI las categorias.
            url = '/inventario/api/reportes/existencia/?format=json';
          }
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }   

      //Existencia de Productos (filtros: Almacen, producto)
      function existenciaByProducto(almacen, producto) {
        var deferred = $q.defer();

        if (almacen != '*') {
          if(producto != undefined) {
            url = '/inventario/api/reportes/existencia/?format=json&almacen=@almacen&producto=@producto'.replace('@almacen', almacen).replace('@producto',producto);
          } else {
            url = '/inventario/api/reportes/existencia/?format=json&almacen=@almacen'.replace('@almacen', almacen);
          }
        } else {
            url = '/inventario/api/reportes/existencia/?format=json&producto=@producto'.replace('@producto',producto);
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }      

      //Existencia de Productos para Conteo Fisico (filtros: Almacen, categorias)
      function existenciaConteoFisico(almacen, categorias) {
        var deferred = $q.defer();
        var stringCategorias = "";

        for(i=0; i<categorias.length; i++) {
          stringCategorias += categorias[i]['id'].toString() + ",";
        }
        
        url = '/inventario/api/reportes/existencia/conteoFisico/?format=json&categorias=@categorias&almacen=@almacen'.replace('@categorias',stringCategorias).replace('@almacen', almacen);

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Movimiento de Producto (filtros: Producto, Fecha Inicio, Fecha Fin)
      function movimientoArticulo(Prod, fechaI, fechaF, almacen) {
        var deferred = $q.defer();

        var fechaIn = fechaI.split('/');
        var fechaInicio = fechaIn[2] + '-' + fechaIn[1] + '-' + fechaIn[0];
        
        var fechaFn = fechaF.split('/');
        var fechaFin = fechaFn[2] + '-' + fechaFn[1] + '-' + fechaFn[0];

        url = '/api/inventario/movimiento/{Prod}/{fechaI}/{fechaF}/{almacen}/?format=json'.replace('{Prod}', Prod)
              .replace('{fechaI}', fechaInicio).replace('{fechaF}', fechaFin).replace('{almacen}', almacen);

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }   

      return {
        all : all,
        existencia : existencia,
        existenciaByProducto : existenciaByProducto,
        categorias : categorias,
        existenciaConteoFisico : existenciaConteoFisico,
        movimientoArticulo : movimientoArticulo
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('RPTMovimientoArticuloCtrl', ['$scope', '$filter', 'InventarioService', 'InventarioServiceRPT', 
                                              function ($scope, $filter, InventarioService, InventarioServiceRPT) {

      //Traer productos
      $scope.getProducto = function($event) {
        $event.preventDefault();
        var descrp = '';

        if($event.type != 'click') {
          descrp = $scope.producto;
        }

        InventarioService.productos(descrp).then(function (data) {

          if(data.length > 0){
            $scope.productos = data;

            $scope.tableProducto = true;
            $scope.productoNoExiste = '';
          } else {
            $scope.tableProducto = false;
            $scope.productoNoExiste = 'No existe el producto'
          }
        });
      }

      //Agregar Producto
      $scope.addProducto = function($event, Prod) {
        $event.preventDefault();

        $scope.producto = Prod.descripcion;
        $scope.codigoProducto = Prod.codigo;
        $scope.tableProducto = false;
      }

      //Traer almacenes
      $scope.getAlmacenes = function() {
        InventarioService.almacenes().then(function (data) {
          $scope.almacenes = data;
        });
      }

      //Generar reporte
      $scope.movimiento = function($event) {
        $event.preventDefault();

        try {
          InventarioServiceRPT.movimientoArticulo($scope.codigoProducto, $scope.desdeFecha, $scope.hastaFecha, $scope.almacen).then(function (data) {
            $scope.resultados = data;
          },
          function () {
            throw data;
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

    }])

    
    //****************************************************
    //CONTROLLERS Existencia                             *
    //****************************************************
    .controller('RPTExistenciaArticuloCtrl', ['$scope', '$filter', 'InventarioServiceRPT', 'InventarioService',
                                                function ($scope, $filter, InventarioServiceRPT, InventarioService) {

      // Inicializacion de Variables
      $scope.iconcheck = 'icon-checkbox-unchecked';
      $scope.regAll = true;
      $scope.categoriasSeleccionadas = [];
      $scope.reg = [];
      $scope.valoresChk = [];

      $scope.mostrarCategorias = true;
      $scope.almacen = '*';
      $scope.busquedaValor = 'producto';

      $scope.toggleCategorias = function() {
        $scope.mostrarCategorias = !$scope.mostrarCategorias;
      }

      // Funcion para mostrar error por pantalla
      $scope.mostrarError = function(error) {
        $scope.errorMsg = error;
        $scope.errorShow = true;
      }

      // Mostrar/Ocultar error
      $scope.toggleError = function() {
        $scope.errorShow = !$scope.errorShow;
      }

      //Cuando se le de click al checkbox de categorias.
      $scope.seleccionAll = function() {

        $scope.categorias.forEach(function (data) {
          if ($scope.regAll === true){

            $scope.valoresChk[data.id] = true;
            $scope.categoriasSeleccionadas.push(data);
          }
          else{

            $scope.valoresChk[data.id] = false;
            $scope.categoriasSeleccionadas.splice(data);
          }
        });

        if($scope.regAll === false) {
          $scope.regAll = true;
          $scope.iconcheck = 'icon-checkbox-unchecked';
        } else {
          $scope.regAll = false;
          $scope.iconcheck = 'icon-checkbox-checked';
        }
      }

      //Cuando se le de click a un checkbox de la lista
      $scope.selectedReg = function(iReg) {
        
        index = $scope.categorias.indexOf(iReg);

        if ($scope.reg[$scope.categorias[index].id] === true){
          $scope.categoriasSeleccionadas.push($scope.categorias[index]);
        }
        else{
          $scope.categoriasSeleccionadas = _.without($scope.categoriasSeleccionadas, _.findWhere($scope.categoriasSeleccionadas, {id : iReg.id}));
        }
      }

      // Traer registros de existencia (Filtros: almacen, categorias)
      $scope.existencia = function() {
        try {
          if($scope.busquedaValor == 'categoria') {

            InventarioServiceRPT.existencia($scope.almacen, $scope.categoriasSeleccionadas).then(function (data) {
              $scope.registros = data;
            });
          } else {
            InventarioServiceRPT.existenciaByProducto($scope.almacen, $scope.producto).then(function (data) {
              $scope.registros = data;
            });
          }
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      // Buscar existencia por producto <ENTER>
      $scope.existenciaPorProducto = function($event) {
        if($event.keyCode == 13) {
          $scope.existencia();
        }
      }

      $scope.getCategoriasProductos = function() {
        InventarioServiceRPT.categorias().then(function (data) {
          $scope.categorias = data;
        });
      }

      $scope.getAlmacenes = function() {
        InventarioService.almacenes().then(function (data) {
          var almacenes = [];
          var todos = new Object();

          todos.id = '*';
          todos.descripcion = 'TODOS';
          almacenes.push(todos);
          almacenes = almacenes.concat(data);

          $scope.almacenes = almacenes;
        });
      }

      //Traer productos
      $scope.getProducto = function($event) {
        $event.preventDefault();
        var descrp = '';

        if($event.type != 'click') {
          descrp = $scope.producto;
        }

        InventarioService.productos(descrp).then(function (data) {
          if(data.length > 0){
            $scope.productos = data;

            $scope.tableProducto = true;
            $scope.productoNoExiste = '';
          } else {
            $scope.tableProducto = false;
            $scope.productoNoExiste = 'No existe el producto'
          }
        });
      }

      // Traer registros de existencia para Conteo Fisico (Filtros: almacen, categorias)
      $scope.existenciaConteoFisico = function() {
        try {
          InventarioServiceRPT.existenciaConteoFisico($scope.almacen, $scope.categoriasSeleccionadas).then(function (data) {
            $scope.registros = data;
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

    }]);

})(_);  