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

      //Eliminar Entrada Inventario
      function eliminarEI(entradaNo) {
        var deferred = $q.defer();

        $http.post('/inventario/eliminar/', JSON.stringify({'entradaNo': entradaNo})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Guardar Ajuste Inventario
      function guardarAjusteInv(dataH, dataD, fecha) {
        var deferred = $q.defer();

        $http.post('/inventario/ajuste/', JSON.stringify({'cabecera': dataH, 'detalle': dataD, 'fecha': fecha})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Procesar Ajuste de Inventario
      function procesarAjusteInv(ajusteNo) {
        var deferred = $q.defer();

        $http.post('/inventario/procesarAjuste/', JSON.stringify({'ajusteNo': ajusteNo})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Guardar Transferencia Inventario
      function guardarTransfInv(almacenO, almacenD, prod, cantidad) {
        var deferred = $q.defer();

        $http.post('/inventario/transferencia/', JSON.stringify({'almacenOrigen': almacenO, 'almacenDestino': almacenD, 
                                                                  'producto': prod, 'cantidadTransferir': cantidad})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Llenar el listado de entradas de inventario
      function allEntradas() {
        var deferred = $q.defer();

        $http.get('/api/inventario/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Llenar el listado de Ajustes de inventario
      function AjustesInvListado() {
        var deferred = $q.defer();

        $http.get('/api/ajustesInventario/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Llenar el listado de Transferencias de Almacenes
      function TransfInvListado() {
        var deferred = $q.defer();

        $http.get('/api/transfAlmacenes/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un ajuste de inventario en especifico (Desglose)
      function AjusteInvById(NoDoc) {
        var deferred = $q.defer();

        var doc = NoDoc != undefined? NoDoc : 0;

        $http.get('/inventario/ajustejson/?numero={NoDoc}&format=json'.replace('{NoDoc}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Llenar el listado de entradas de inventario
      function allEntradasByTipo(tipo) {
        var deferred = $q.defer();

        allEntradas().then(function (data) {
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
        allEntradas().then(function (data) {
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

        allEntradas().then(function (data) {
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

      //Llenar el listado de salidas de inventario
      function allSalidas() {
        var deferred = $q.defer();

        $http.get('/api/inventariosalidas/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      // Dar Salida a Inventario
      function SalidaInv(cabecera, detalle, almacen) {
        var deferred = $q.defer();

        $http.post('/inventario/salida/', JSON.stringify({'cabecera': cabecera, 'detalle': detalle, 'almacen': almacen})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Eliminar Salida Inventario
      function eliminarSI(salidaNo) {
        var deferred = $q.defer();

        $http.post('/inventario/salida/eliminar/', JSON.stringify({'salidaNo': salidaNo})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar por tipo de posteo (Salidas)
      function SalidasByPosteo(valor){
        var deferred = $q.defer();

        allSalidas().then(function (data) {
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

      //Buscar un documento en especifico (Desglose) -- Salida
      function DocumentoSalidaById(NoDoc) {
        var deferred = $q.defer();

        var doc = NoDoc != undefined? NoDoc : 0;

        $http.get('/inventariosalidajson/?nodoc={NoDoc}&format=json'.replace('{NoDoc}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un numero de documento de salida en especifico en listado de documentos
      function byNoDocSalida(NoDoc) {
        var deferred = $q.defer();
        allSalidas().then(function (data) {
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


      return {
        allEntradas             : allEntradas,
        byPosteo                : byPosteo,
        byNoDoc                 : byNoDoc,
        suplidores              : suplidores,
        productos               : productos,
        guardarEI               : guardarEI,
        almacenes               : almacenes,
        DocumentoById           : DocumentoById,
        getExistenciaByProducto : getExistenciaByProducto,
        SalidaInv               : SalidaInv,
        allEntradasByTipo       : allEntradasByTipo,
        guardarAjusteInv        : guardarAjusteInv,
        AjustesInvListado       : AjustesInvListado,
        AjusteInvById           : AjusteInvById,
        guardarTransfInv        : guardarTransfInv,
        TransfInvListado        : TransfInvListado,
        allSalidas              : allSalidas,
        SalidasByPosteo         : SalidasByPosteo,
        DocumentoSalidaById     : DocumentoSalidaById,
        eliminarEI              : eliminarEI,
        eliminarSI              : eliminarSI,
        byNoDocSalida           : byNoDocSalida,
        procesarAjusteInv       : procesarAjusteInv
      };

    }])


    //****************************************************
    //CONTROLLERS    ENTRADA DE INVENTARIO               *
    //****************************************************
    .controller('ListadoEntradaInvCtrl', ['$scope', '$filter', '$window', '$rootScope', 'appService', 'InventarioService', 
                                          function ($scope, $filter, $window, $rootScope, appService, InventarioService) {
      
      //Inicializacion de variables
      $scope.mostrar = 'mostrar';
      $scope.tipoinv = "E";
      $scope.posteof = '*';
      $scope.errorShow = false;
      $scope.showLEI = true;
      $scope.showEI = false;
      $scope.regAll = false;
      $scope.tableProducto = false;
      $scope.condicionBool = true;

      $scope.item = {};
      $scope.entradas = {};
      $scope.dataH = {};

      $scope.desgloseCuentas = [];
      $scope.entradasSeleccionadas = [];
      $scope.reg = [];
      $scope.valoresChk = [];
      $scope.dataD = [];

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLEI = 'UpArrow';

      // Cuentas
      $scope.cuentasBuscar = function($event) {

        appService.allCuentasContables().then(function (data) {
          if(data.length > 0) {
            console.log(data);
            $scope.cuentasContables = data
            $scope.tableCuenta = true;
          }
        });
      }

      // Mostrar/Ocultar panel de Listado de Entrada Inventario
      $scope.toggleLEI = function() {
        $scope.showLEI = !$scope.showLEI;

        if($scope.showLEI === true) {
          $scope.ArrowLEI = 'UpArrow';
          $scope.showEI = false;
        } else {
          $scope.ArrowLEI = 'DownArrow';
          $scope.showEI = true;
        }
      }

      // Mostrar/Ocultar panel de listado de Salida de Inventario
      $scope.toggleLEI = function() {
        $scope.showLEI = !$scope.showLEI;

        if($scope.showLEI === true) {
          $scope.ArrowLEI = 'UpArrow';
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

      // Mostrar/Ocultar posteo Contabilidad
      $scope.toggleInfo = function() {
        $scope.showPostear = !$scope.showPostear;
      }

      //Listado de todas las entradas de inventario
      $scope.listadoEntradas = function() {
        $scope.mostrar = 'mostrar';
        $scope.NoFoundDoc = '';
        $scope.entradasSeleccionadas = [];
        $scope.valoresChk = [];
        $scope.regAll = false;

        try {
          InventarioService.allEntradas().then(function (data) {
            $scope.entradas = data;

            if(data.length > 0) {
              $scope.verTodos = 'ver-todos-ei';

              var i = 0;
              data.forEach(function (data) {
                $scope.valoresChk[i] = false;
                i++;
              });
            
              $scope.mostrar = 'ocultar';
            }

          }, function() {
              $scope.mostrar = 'ocultar';
          });
        } catch (e) {
          $scope.mostrarError(e);
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

      //Eliminar Entrada de Inventario (Borra el detalle y pone ELIMINADO, pero el registro sigue en base de datos)
      $scope.eliminarEntradaInv = function($event) {
        $event.preventDefault();

        try {
          InventarioService.eliminarEI($scope.dataH.entradaNo).then(function (data) {
            if(data == 1) {
              $scope.errorShow = false;
              $scope.listadoEntradas();
              $scope.nuevaEntrada();
              $scope.toggleLEI();
            } else {
              $scope.mostrarError(data);
            }
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      // Visualizar Documento (Entrada de Inventario Existente - desglose)
      $scope.DocFullById = function(NoDoc) {
        try {

          InventarioService.DocumentoById(NoDoc).then(function (data) {
            //completar los campos
            $scope.nuevaEntrada();

            if(data.length > 0) {
              $scope.showLEI = false;
              $scope.showEI = true;

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
              $scope.dataH.borrado = data[0]['borrado'];
              $scope.dataH.borradoPor = data[0]['borradoPor'];
              $scope.dataH.borradoFecha = data[0]['borradoFecha'];

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
        
        $scope.dataH = {};
        $scope.dataD = [];
        $scope.productos = [];

        $scope.showLEI = false;
        $scope.showEI = true;

        $scope.ArrowLEI = 'DownArrow';
        $scope.dataH.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
        $scope.dataH.usuario = usuario;
        $scope.dataH.condicion = 'CO';
        $scope.dataH.posteo = 'N';
        $scope.dataH.borrado = false;


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
        } else {
          $scope.errorShow = false;
        }

        //No agregar el producto si ya existe
        $scope.dataD.forEach(function (item) {
          if(item.codigo == Prod.codigo) {
            $scope.mostrarError("No puede agregar mas de una vez el producto : " + item.descripcion);
            throw "No puede agregar mas de una vez el producto : " + item.descripcion;
          }
        });

        $scope.existenciaProducto(Prod.codigo, $scope.almacen);

        Prod.cantidad = 1;
        $scope.dataD.push(Prod);
        $scope.tableProducto = false;

        $scope.calculaTotales();
      }

      //Cuando se le de click al checkbox del header.
      $scope.seleccionAll = function() {
        $scope.entradasSeleccionadas = [];

        $scope.entradas.forEach(function (data) {
          if (data.posteo == 'N' && data.borrado == false) {
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
          $scope.entradasSeleccionadas = _.without($scope.entradasSeleccionadas, _.findWhere($scope.entradasSeleccionadas, {id : iReg.id}));
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

        $window.sessionStorage['entrada'] = JSON.stringify(entrada);
        $window.open('/inventario/print/{entrada}'.replace('{entrada}',entrada.id), target='_blank'); 
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

      //Funcion para postear los registros seleccionados. (Postear es llevar al Diario)
      $scope.postear = function(){
        var idoc = 0;
        $scope.iDocumentos = 0;
        $scope.totalDebito = 0.00;
        $scope.totalCredito = 0.00;

        $scope.showPostear = true;
        $scope.desgloseCuentas = [];

        appService.getDocumentoCuentas('EINV').then(function (data) {
          $scope.documentoCuentas = data;
  
          //Prepara cada linea de posteo
          $scope.entradasSeleccionadas.forEach(function (item) {
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

    }])
  
  //****************************************************
  //CONTROLLERS PRINT DOCUMENT ENTRADA DE INVENTARIO   *
  //****************************************************
  .controller('ImprimirInventarioCtrl', ['$scope', '$filter', '$window', 'InventarioService', function ($scope, $filter, $window, InventarioService) {
    $scope.entrada = JSON.parse($window.sessionStorage['entrada']);

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
        total += item.costo * (item.cantidad);
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

  }])

    //****************************************************
    //CONTROLLERS  TRANSFERENCIA INVENTARIO              *
    //****************************************************
    .controller('TransfInvCtrl', ['$scope', '$filter', '$window', '$rootScope', 'InventarioService', 
                                  function ($scope, $filter, $window, $rootScope, InventarioService) {
      
      //Inicializacion de variables
      $scope.mostrar = 'mostrar';
      $scope.errorShow = false;
      $scope.showLEI = true;
      $scope.regAll = false;
      $scope.tableProducto = false;
      $scope.condicionBool = true;

      $scope.item = {};
      $scope.entradas = {};
      $scope.dataH = {};

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLEI = 'UpArrow';

      // Mostrar/Ocultar error
      $scope.toggleError = function() {
        $scope.errorShow = !$scope.errorShow;
      }

      // Funcion para mostrar error por pantalla
      $scope.mostrarError = function(error) {
        $scope.errorMsg = error;
        $scope.errorShow = true;
      }

      $scope.getAlmacen = function() {
        InventarioService.almacenes().then(function (data) {
          $scope.almacenes = data;
        });
      }      

      //Listado de Ajustes de Inventario
      $scope.ListadoTransfAlmacenes = function() {
        InventarioService.TransfInvListado().then(function (data) {
          $scope.transferencias = data;
        });
      }     

      //Traer productos
      $scope.getProducto = function($event) {
        $event.preventDefault();
        var descrp = '';

        if($event.type != 'click') {
          descrp = $scope.producto;
        }

        try {
          InventarioService.productos(descrp).then(function (data) {

            if(data.length > 0){
              $scope.productos = data;

              $scope.tableProducto = true;
              $scope.productoNoExiste = '';
            } else {
              $scope.tableProducto = false;
              $scope.productoNoExiste = 'No existe el producto'
            }
          }, function() {
            $scope.mostrarError('No pudo traer los productos');
            throw "PRODUCTOS ERROR";
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }
     
      //Agregar Producto
      $scope.addProducto = function($event, Prod) {
        $event.preventDefault();

        try {

          $scope.validaAlmacenes();

          $scope.codigoProducto = Prod.codigo;
          $scope.producto = Prod.descripcion;

          //Obtener existencias de ambos almacenes
          $scope.getExistencias($scope.codigoProducto);

          $scope.tableProducto = false;
          $scope.errorShow = false;

        } catch(e) {
          $scope.mostrarError(e);
        }
      }

      $scope.validaAlmacenes = function() {
        if ($scope.dataH.almacenOrigen == undefined || $scope.dataH.almacenOrigen == '') {
            throw "Debe seleccionar un almacen de Origen";
          }

          if ($scope.dataH.almacenDestino == undefined || $scope.dataH.almacenDestino == '') {
            throw "Debe seleccionar un almacen de Destino";
          }

          if ($scope.dataH.almacenOrigen == $scope.dataH.almacenDestino) {
            throw "El almacen ORIGEN y el almacen DESTINO no pueden ser el mismo.";
          }
      }

      $scope.getExistencias = function(producto) {

        //Buscar existencia en almacen ORIGEN
        InventarioService.getExistenciaByProducto(producto, $scope.dataH.almacenOrigen).then(function (data) {
          if(data.length > 0) {
            $scope.existencia1 = data[0]['cantidad'];
          } else {
            $scope.existencia1 = '';
          }
        });

        //Buscar existencia en almacen DESTINO
        InventarioService.getExistenciaByProducto(producto, $scope.dataH.almacenDestino).then(function (data) {
          if(data.length > 0) {
            $scope.existencia2 = data[0]['cantidad'];
          } else {
            $scope.existencia2 = '';
          }
        });
      }

      //Cantidad a Transferir - field
      $scope.cantidadTransferir = function($event) {
        try {
          if(parseFloat($scope.cntTransf) > parseFloat($scope.existencia1)) {
            $scope.cntTransf = '';
            throw "La cantidad a TRANSFERIR no puede exceder a la cantidad ORIGEN.";
          } else {
            $scope.errorShow = false;
          }
        } catch(e) {
          $scope.mostrarError(e);
        }
      }

      $scope.nuevaTransf = function () {
        $scope.dataH = {};
        $scope.codigoProducto = '';
        $scope.producto = '';
        $scope.existencia1 = '';
        $scope.existencia2 = '';
        $scope.cntTransf = '';
      }

      $scope.refrescar = function () {
        if ($scope.codigoProducto != undefined && $scope.codigoProducto != '') {
          $scope.getExistencias($scope.codigoProducto);
        }
      }

      //Guardar Transferencia de Inventario
      $scope.guardarTransfInv = function() {
        try {
          
          $scope.validaAlmacenes();
          $scope.cantidadTransferir(null);

          if($scope.TransfForm.$valid) {
            InventarioService.guardarTransfInv($scope.dataH.almacenOrigen, $scope.dataH.almacenDestino, 
                                                $scope.codigoProducto, $scope.cntTransf).then(function (data) {
              if(data.length > 0) {
                $scope.refrescar();
                $scope.ListadoTransfAlmacenes();
              }
            });
          } else {
            $scope.mostrarError('Verifique que completo todos los campos requeridos.');
          }
        } catch(e) {
          $scope.mostrarError(e);
        }
      }

    }])

  //****************************************************
  //CONTROLLERS AJUSTE DE INVENTARIO                   *
  //****************************************************
  .controller('AjusteInvCtrl', ['$scope', '$filter', 'InventarioService', function ($scope, $filter, InventarioService) {

    //Inicializacion de variablaes
    $scope.tableProducto = false;
    $scope.dataH = {};
    $scope.dataD = [];
    $scope.dataH.numero = 0;
    $scope.showLAI = true;
    $scope.ArrowLAI = 'UpArrow'
    document.getElementById('botonGuardar').style.display = 'None';

    $scope.mostrar = 'ocultar';
    
    $scope.toggleLAI = function() {
      $scope.showLAI = !$scope.showLAI;

      if($scope.showLAI === true){
        $scope.ArrowLAI = 'UpArrow';
      } else {
        $scope.ArrowLAI = 'DownArrow';
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
    }

    $scope.getAlmacen = function() {
      InventarioService.almacenes().then(function (data) {
        $scope.almacenes = data;
      });
    }     

    //Listado de Ajustes de Inventario
    $scope.ListadoAjustes = function() {
      InventarioService.AjustesInvListado().then(function (data) {
        $scope.ajustes = data;
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

    //Agregar Producto
    $scope.addProducto = function($event, Prod) {
      $event.preventDefault();

      if ($scope.almacen == undefined || $scope.almacen == '') {
        $scope.mostrarError('Debe seleccionar un almacen');
        throw "almacen";
      } else {
        $scope.errorShow = false;
      }

      InventarioService.getExistenciaByProducto(Prod.codigo, $scope.almacen).then(function (data) {
        if(data.length > 0) {
          Prod.cantidadTeorico = $filter('number')(data[0]['cantidad'], 2);
        } else {
          Prod.cantidadTeorico = 0;
        }
      });

      Prod.cantidad = 0;
      Prod.almacen = $scope.almacen;

      $scope.dataD.push(Prod);
      $scope.tableProducto = false;

      // $scope.calculaTotales();
    }

   //Eliminar producto de la lista de entradas
    $scope.delProducto = function($event, prod) {
      $event.preventDefault();
      
      try {
        $scope.dataD = _.without($scope.dataD, _.findWhere($scope.dataD, {codigo: prod.codigo}));

        // $scope.calculaTotales();
        
      } catch (e) {
        $scope.mostrarError(e);
      }
    }

    //Guardar Ajuste de Inventario
    $scope.guardarAjusteInv = function() {

      try {
        if($scope.dataH.fecha != undefined) {
          var fechaP = $scope.dataH.fecha.split('/');
          var fechaFormatted = fechaP[2] + '-' + fechaP[1] + '-' + fechaP[0];
        }

        if($scope.AjusteForm.$valid) {
          InventarioService.guardarAjusteInv($scope.dataH, $scope.dataD, fechaFormatted).then(function (data) {
            if(data.length > 0) {
              $scope.ListadoAjustes();
              $scope.nuevoAjuste();
            }
          });
        } else {
          $scope.mostrarError('Verifique que completo todos los campos requeridos.');
        }
      } catch(e) {
        $scope.mostrarError(e);
      }
    }

    //Procesar Ajustes de Inventario
    $scope.procesarAjuste = function(ajusteNo) {
      InventarioService.procesarAjusteInv(ajusteNo).then(function (data) {
        if(data == 1) {
          alert('El ajuste de inventario fue procesado!');
          $scope.ListadoAjustes();
        } else {
          $scope.mostrarError(data);
        }
      });
    }     

    // Limpiar los campos (Nuevo)
    $scope.clearFields = function($event) {
      $event.preventDefault();

      $scope.nuevoAjuste();
    }
    
    // Nuevo Registro de Ajuste de Inventario
    $scope.nuevoAjuste = function() {
      $scope.dataH = {};
      $scope.dataD = [];
      $scope.dataH.numero = 0;
      $scope.producto = '';
      $scope.dataH.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      document.getElementById('botonGuardar').style.display = '';

      if($scope.showLAI == true) {
        $scope.toggleLAI();
      }
    }

    // Visualizar Documento (Ajuste de Inventario Existente - desglose)
    $scope.DocFullById = function(NoDoc) {
      try {

        InventarioService.AjusteInvById(NoDoc).then(function (data) {
          //completar los campos
          $scope.nuevoAjuste();

          if(data.length > 0) {
            $scope.errorMsg = '';
            $scope.errorShow = false;

            $scope.dataH.numero = $filter('numberFixedLen')(NoDoc, 8);
            $scope.dataH.fecha = $filter('date')(data[0]['fecha'], 'dd/MM/yyyy');
            $scope.dataH.notaAjuste = data[0]['notaAjuste'];
            $scope.dataH.estatus = data[0]['estatus'];
            $scope.dataH.usuario = data[0]['usuario'];
            $scope.dataH.datetimeServer = data[0]['datetimeServer'];

            data[0]['productos'].forEach(function (item) {
              $scope.dataD.push(item);
            })
            // $scope.calculaTotales();
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
  }])

    //****************************************************
    //CONTROLLERS   SALIDA DE INVENTARIO                 *
    //****************************************************
    .controller('ListadoSalidaInvCtrl', ['$scope', '$filter', '$window', '$rootScope', 'appService','InventarioService', 
                                          function ($scope, $filter, $window, $rootScope, appService, InventarioService) {
      
      //Inicializacion de variables
      $scope.mostrar = 'mostrar';
      $scope.posteof = '*';
      $scope.errorShow = false;
      $scope.showLSI = true;
      $scope.showSI = false;
      $scope.tableProducto = false;
      $scope.condicionBool = true;

      $scope.item = {};
      $scope.entradas = {};
      $scope.dataH = {};

      $scope.dataD = [];

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLSI = 'UpArrow';

      // Mostrar/Ocultar panel de Listado de Salida Inventario
      $scope.toggleLSI = function() {
        $scope.showLSI = !$scope.showLSI;

        if($scope.showLSI === true) {
          $scope.ArrowLSI = 'UpArrow';
          $scope.showSI = false;
        } else {
          $scope.ArrowLSI = 'DownArrow';
          $scope.showSI = true;
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
      }

      // Mostrar/Ocultar posteo Contabilidad
      $scope.toggleInfo = function() {
        $scope.showPostear = !$scope.showPostear;
      }

      //Listado de todas las salidas de inventario
      $scope.listadoSalidas = function(tipo) {
        $scope.mostrar = 'mostrar';
        $scope.NoFoundDoc = '';

        try {
          InventarioService.allSalidas().then(function (data) {
            $scope.salidas = data;

            if(data.length > 0) {
              $scope.verTodos = 'ver-todos-ei';
            }

            $scope.mostrar = 'ocultar';
          }, function() {
              $scope.mostrar = 'ocultar';
          });
        } catch (e) {
          $scope.mostrarError(e);
        } 
      }

      //Filtrar las salidas de inventario por posteo (SI/NO)
      $scope.filtrarPosteoSalidas = function() {
        try {

          if($scope.posteof != '*') {
            InventarioService.SalidasByPosteo($scope.posteof).then(function (data) {
              $scope.salidas = data;

              if(data.length > 0){
                $scope.verTodos = '';
              }
            });
          } else {
            $scope.listadoSalidas();
          }        
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Guardar Salida Inventario
      $scope.guardarSI = function() {
        try {
          if (!$scope.SalidaInventarioForm.$valid) {
            throw "Verifique que todos los campos esten completados correctamente.";
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

          InventarioService.guardarSI(dataH,$scope.dataD,$scope.almacen).then(function (data) {
            if (data != '1') {
              $scope.mostrarError(data);
              throw data;
            } else {
              $scope.errorShow = false;
              $scope.listadoSalidas('E');

              $scope.nuevaSalida();
              $scope.toggleLSI();
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

      // Visualizar Documento (Salida de Inventario Existente - desglose)
      $scope.DocFullById = function(NoDoc) {
        try {

          InventarioService.DocumentoSalidaById(NoDoc).then(function (data) {
            //completar los campos
            $scope.nuevaSalida();

            if(data.length > 0) {
              $scope.showLSI = false;
              $scope.showSI = true;

              $scope.errorMsg = '';
              $scope.errorShow = false;

              $scope.dataH.salidaNo = $filter('numberFixedLen')(NoDoc, 8);
              $scope.dataH.fecha = $filter('date')(data[0]['fecha'],'dd/MM/yyyy');
              $scope.dataH.nota = data[0]['descripcionSalida'];
              $scope.dataH.usuario = data[0]['usuarioSalida'];
              $scope.dataH.borrado = data[0]['borrado'];
              $scope.dataH.borradoPor = data[0]['borradoPor'];

              data[0]['productos'].forEach(function (item) {
                $scope.dataD.push(item);
                $scope.almacen = item['almacen'];
              })
              
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

      //Nueva Salida de Inventario
      $scope.nuevaSalida = function(usuario) {
        $scope.producto = '';
        $scope.almacen = '';
        $scope.subtotal = '';
        $scope.total = '';
        
        $scope.dataH = {};
        $scope.dataD = [];
        $scope.productos = [];

        $scope.showLSI = false;
        $scope.showSI = true;
        $scope.errorShow = false;

        $scope.ArrowLSI = 'DownArrow';
        $scope.dataH.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
        $scope.dataH.usuario = usuario;
        $scope.dataH.condicion = 'CO';
        $scope.dataH.posteo = 'N';
        $scope.dataH.salidaNo = '0';
        $scope.dataH.borrado = false;

        $scope.disabledButton = 'Boton';

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

      //Agregar Producto
      $scope.addProducto = function($event, Prod) {
        $event.preventDefault();

        if ($scope.almacen == undefined || $scope.almacen == '') {
          $scope.mostrarError('Debe seleccionar un almacen');
          throw "almacen";
        } else {
          $scope.errorShow = false;
        }

        //No agregar el producto si ya existe
        $scope.dataD.forEach(function (item) {
          if(item.codigo == Prod.codigo) {
            $scope.mostrarError("No puede agregar mas de una vez el producto : " + item.descripcion);
            throw "No puede agregar mas de una vez el producto : " + item.descripcion;
          }
        });

        $scope.existenciaProducto(Prod.codigo, $scope.almacen);

        Prod.cantidad = 1;
        $scope.dataD.push(Prod);
        $scope.tableProducto = false;

        $scope.calculaTotales();
      }
      
      //Dar Salida a productos.
      $scope.darSalidaInv = function() {
        try {
          if($scope.SalidaInventarioForm.$valid == true){
            
            InventarioService.SalidaInv($scope.dataH, $scope.dataD, $scope.almacen).then(function (data) {
              if(data == 1) {
                $scope.errorShow = false;
                $scope.showSI = false;
                $scope.showLSI = true;
                $scope.listadoSalidas();
              } else {
                $scope.mostrarError(data);
              }
            });
          } else {
            $scope.mostrarError("Verifique que todos los campos esten completados correctamente.");
          }
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Eliminar Salida de Inventario (Borra el detalle y pone ELIMINADO, pero el registro sigue en base de datos)
      $scope.eliminarSalidaInv = function($event, salidaNo) {
        $event.preventDefault();

        try {
          InventarioService.eliminarSI(salidaNo).then(function (data) {
            if(data == 1) {
              $scope.errorShow = false;
              $scope.listadoSalidas();
              $scope.nuevaSalida();
              $scope.toggleLSI();
            } else {
              $scope.mostrarError(data);
            }
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Buscar una salida de inventario en especifico
      $scope.filtrarPorNoDocSalida = function(NoDoc) {
        try {
          InventarioService.byNoDocSalida(NoDoc).then(function (data) {
            $scope.salidas = data;

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
        }
      }

      //Buscar Documento por ENTER
      $scope.buscarDocSalida = function($event, NoDoc) {
        if($event.keyCode == 13) {
          $scope.filtrarPorNoDocSalida(NoDoc);
        }
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

      //Funcion para postear los registros seleccionados. (Postear es llevar al Diario)
      $scope.postear = function(salidaItem){
        var idoc = 0;
        $scope.iDocumentos = 0;
        $scope.totalDebito = 0.00;
        $scope.totalCredito = 0.00;

        $scope.showPostear = true;
        $scope.desgloseCuentas = [];

        appService.getDocumentoCuentas('SINV').then(function (data) {
          $scope.documentoCuentas = data;

          //Prepara cada linea de posteo
          $scope.documentoCuentas.forEach(function (documento) {
            var desgloseCuenta = new Object();
            if (documento.accion == 'D') {
              $scope.totalDebito += parseFloat(salidaItem.totalGeneral.toString().replace('$','').replace(',',''));
            } else {
              $scope.totalCredito += parseFloat(salidaItem.totalGeneral.toString().replace('$','').replace(',',''));
            }

            desgloseCuenta.cuenta = documento.getCuentaCodigo;
            desgloseCuenta.descripcion = documento.getCuentaDescrp;
            desgloseCuenta.ref = documento.getCodigo + salidaItem.id;
            desgloseCuenta.debito = documento.accion == 'D'? salidaItem.totalGeneral.toString().replace('$','') : $filter('number')(0.00, 2);
            desgloseCuenta.credito = documento.accion == 'C'? salidaItem.totalGeneral.toString().replace('$','') : $filter('number')(0.00, 2);

            $scope.desgloseCuentas.push(desgloseCuenta);
          });
        });
      }

    }])

})(_);  