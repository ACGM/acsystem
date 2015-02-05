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

      //Llenar el listado de entradas de inventario
      function allByTipo(tipo) {
        var deferred = $q.defer();

        all().then(function (data) {
          var results = data.filter(function (item) {
            return item.getTipo == tipo;
          });

          if(results.length > 0) {
            deferred.resolve(results);
          } else {
            deferred.reject();
          }
        });

        return deferred.promise;
      }

      //Existencia de Producto
      function getExistenciaByProducto(producto, almacen) {
        var deferred = $q.defer();
        url = '/api/producto/existencia/{producto}/{almacen}/?format=json'.replace('{producto}',producto).replace('{almacen}',almacen);

        $http.get(url)
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
      function suplidores(nombre) {
        var deferred = $q.defer();

        if(nombre != undefined && nombre != '') {
          url = '/api/suplidor/nombre/{nombre}/?format=json'.replace('{nombre}',nombre);
        } else {
          url = '/api/suplidor/?format=json';
        }

        $http.get(url)
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
      function productos(descrp) {
        var deferred = $q.defer();

        if(descrp != undefined && descrp != '') {
          url = '/api/producto/descripcion/{descrp}/?format=json'.replace('{descrp}',descrp)
        } else {
          url = '/api/producto/?format=json';
        }

        $http.get(url)
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

      // Dar Salida a Inventario
      function SalidaInv(entradaNo, nota) {
        var deferred = $q.defer();

        $http.post('/inventario/salida/', JSON.stringify({'entradaNo': entradaNo, 'nota': nota})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      return {
        all                     : all,
        byPosteo                : byPosteo,
        byNoDoc                 : byNoDoc,
        suplidores              : suplidores,
        productos               : productos,
        guardarEI               : guardarEI,
        almacenes               : almacenes,
        DocumentoById           : DocumentoById,
        getExistenciaByProducto : getExistenciaByProducto,
        SalidaInv               : SalidaInv,
        allByTipo               : allByTipo
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('ListadoEntradaInvCtrl', ['$scope', '$filter', '$window', 'InventarioService', function ($scope, $filter, $window, InventarioService) {
      
      //Inicializacion de variables
      $scope.tipoinv = "E";
      $scope.posteof = '*';
      $scope.errorShow = false;
      $scope.showLEI = true;
      $scope.showEI = false;
      $scope.showSI = false;
      $scope.regAll = false;
      $scope.tableProducto = false;
      $scope.condicionBool = true;

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
      $scope.listadoEntradas = function(tipo) {
        $scope.NoFoundDoc = '';
        $scope.entradasSeleccionadas = [];
        $scope.valoresChk = [];
        $scope.regAll = false;

        if(tipo == undefined || tipo == 'undefined') {
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
        } else {
          InventarioService.allByTipo(tipo).then(function (data) {
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
              $scope.listadoEntradas('E');

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

      //Traer almacenes
      $scope.darSalidaInv = function() {
        if($scope.SalidaInventarioForm.$valid == true){
          InventarioService.SalidaInv($scope.dataH.entradaNo, $scope.dataH.notaSalida).then(function (data) {
            if(data == 1) {
              $scope.errorShow = false;
              $scope.showSI = false;
              $scope.showLEI = true;
              $scope.listadoEntradas('S');
              $scope.tipoinv = 'S';
            }
          });
        } else {
          $scope.mostrarError('Verifique que puso un comentario de salida.');

        }
      }

       // Visualizar Documento (Entrada de Inventario Existente - desglose)
      $scope.DocFullById = function(NoDoc, tipo) {
        try {

          InventarioService.DocumentoById(NoDoc).then(function (data) {
            //completar los campos
            $scope.nuevaEntrada();

            if(data.length > 0) {
              //Decidir que renglon mostrar
              if(tipo == 'salida') {
                $scope.showSI = true;
                $scope.showLEI = false;
                $scope.showEI = false
              } else {
                $scope.showEI = true;
                $scope.showLEI = false;
                $scope.showSI = false;
              }

              $scope.errorMsg = '';
              $scope.errorShow = false;

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

              $scope.tipoinv = data[0]['tipo'];

              //Datos de salida
              $scope.dataH.descripcionSalida = data[0]['descripcionSalida'];
              $scope.dataH.fechaSalida = data[0]['fechaSalida'];
              $scope.dataH.usuarioSalida = data[0]['usuarioSalida'];

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

      }

      // Calcula los totales para los productos
      $scope.calculaTotales = function() {
        try {
          var total = 0.0;
          var subtotal = 0.0;

          $scope.dataD.forEach(function (item) {
            total += (parseFloat(item.cantidad) * parseFloat(item.costo));
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
        $scope.tipoinv = 'E';
        
        $scope.dataH = {};
        $scope.dataD = [];
        $scope.productos = [];

        $scope.showLEI = false;
        $scope.showSI = false;
        $scope.showEI = true;

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

          if ($scope.dataH.venceDias != undefined && fechaF != 'Invalid Date' && $scope.dataH.venceDias != '') {
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
        var suplidor = '';

        if($event.type != 'click') {
          suplidor = $scope.dataH.suplidorNombre;
        }

        InventarioService.suplidores(suplidor).then(function (data) {

          if(data.length > 0) {
            $scope.suplidores = data;

            $scope.tableSuplidor = true;
            $scope.suplidorNoExiste = '';
          } else {
            $scope.tableSuplidor = false;
            $scope.suplidorNoExiste = 'No existe el suplidor';
          }

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

      //Existencia de Producto
      $scope.existenciaProducto = function(prod, almacen) {

        try {
          InventarioService.getExistenciaByProducto(prod, almacen).then(function (data) {

            if(data.length > 0) {
              if(data[0]['cantidad'] < 11) {
                $scope.mostrarError('El producto ' + prod + ' tiene una existencia de ' + data[0]['cantidad']);
              }
            } else {
              $scope.mostrarError('Este producto (' + prod + ') no tiene existencia.');
              throw data;
            }

          }, function() {
            throw data;
          });
        } catch (e) {
          $scope.mostrarError(e);
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

        if ($scope.almacen == undefined || $scope.almacen == '') {
          $scope.mostrarError('Debe seleccionar un almacen');
          throw "almacen";
        }

        $scope.existenciaProducto(Prod.codigo, $scope.almacen);

        Prod.cantidad = 1;
        $scope.dataD.push(Prod);
        $scope.tableProducto = false;

        $scope.calculaTotales();
      }

      
      // Mostrar/Ocultar panel de Listado de Entrada Inventario
      $scope.toggleLEI = function() {
        $scope.showLEI = !$scope.showLEI;

        if($scope.showLEI === true) {
          $scope.ArrowLEI = 'UpArrow';
          $scope.showSI = false;
          $scope.showEI = false;
        } else {
          $scope.ArrowLEI = 'DownArrow';
          $scope.showEI = true;
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

      $scope.condicion = function() {
        if($scope.dataH.condicion == 'CO') {
          $scope.condicionBool = true;
          $scope.dataH.venceDias = '';
          $scope.dataH.fechaVence = '';
        } else {
          $scope.condicionBool = false;
        }
      }

      //Imprimir entrada de inventario
      $scope.Imprimir = function(entrada) {

        $window.localStorage['entrada'] = JSON.stringify(entrada);
        $window.open('/inventario/print/{entrada}'.replace('{entrada}',entrada.id), target='_blank'); 
      }

      //Funcion para postear los registros seleccionados. (Postear es llevar al Diario)
      $scope.postear = function(){

      }

    }])
  
  //****************************************************
  //CONTROLLERS PRINT DOCUMENT                         *
  //****************************************************
  .controller('ImprimirInventarioCtrl', ['$scope', '$filter', '$window', 'InventarioService', function ($scope, $filter, $window, InventarioService) {
    $scope.entrada = JSON.parse($window.localStorage['entrada']);

    InventarioService.DocumentoById($scope.entrada.id).then(function (data) {
      $scope.hoy = Date.now();
      $scope.entrada = data[0];
      $scope.productos = data[0]['productos'];
      
      $scope.condicion = $scope.entrada.condicion.replace('CR','CREDITO').replace('CO','DE CONTADO');
      $scope.posteo = $scope.entrada.posteo.replace('S', 'POSTEADA').replace('N', 'EN PROCESO');

      if($scope.entrada.diasPlazo != undefined && $scope.entrada.diasPlazo != '') {
        var nextDate = new Date();
        var fechaF = new Date($scope.entrada.fecha);

        nextDate.setDate(fechaF.getDate()+parseInt($scope.entrada.diasPlazo));

        $scope.fechaVence = $filter('date')(nextDate, 'dd/MM/yyyy');

        $scope.totalValor_ = $scope.totalValor();
        $scope.totalCantidad_ = $scope.totalCantidad();
        $scope.totalCantidadAnterior_ = $scope.totalCantidadAnterior();
        $scope.totalCosto_ = $scope.totalCosto();

      }
    });

    $scope.totalValor = function() {
      var total = 0.0;

      $scope.productos.forEach(function (item) {
        total += item.costo * (item.cantidad + item.cantidadAnterior);
      });

      return total;
    }

    $scope.totalCantidad = function() {
      var total = 0.0;

      $scope.productos.forEach(function (item) {
        total += item.cantidad;
      });
      
      return total;
    }

    $scope.totalCantidadAnterior = function() {
      var total = 0.0;

      $scope.productos.forEach(function (item) {
        total += item.cantidadAnterior;
      });
      
      return total;
    }

    $scope.totalCosto = function() {
      var total = 0.0;

      $scope.productos.forEach(function (item) {
        total += parseFloat(item.costo);
      });
      
      return total;
    }

  }]);

})(_);  