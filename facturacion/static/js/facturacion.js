(function (_) {

  angular.module('cooperativa.facturacion', ['ngAnimate'])

    .factory('FacturacionService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Factura
      function guardarFact(dataH, dataD) {
        var deferred = $q.defer();
    
        console.log(dataD);
        $http.post('/facturacion/', JSON.stringify({'cabecera': dataH, 'detalle': dataD})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Eliminar Factura
      function eliminarFACT(facturaNo) {
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

      //Impresion de Factura (incrementa el campo de IMPRESA)
      function impresionFact(fact) {
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

      //Impresion de Reporte de Utilidad
      function reporteUtilidad() {
        var deferred = $q.defer();

        $http.get('/facturacion/reportes/utilidades/'.replace('{fechaI}','fact'), {'fechaF': 'fact'}).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Reporte de Resumen de Ventas
      function resumenVentas(fechaI, fechaF) {
        var deferred = $q.defer();

        $http.get('/facturacion/reportes/ventasResumido/json/?fechaI={fechaI}&fechaF={fechaF}'.replace('{fechaI}', fechaF).replace('{fechaF}', fechaF)).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Postear registros de Facturas.
      function postearFACT(registros) {
        var deferred = $q.defer();

        $http.post('/facturacion/postear-registros/', JSON.stringify({'registros': registros})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
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
        guardarOrdenSC: guardarOrdenSC,
        impresionFact: impresionFact,
        reporteUtilidad : reporteUtilidad,
        resumenVentas : resumenVentas,
        eliminarFACT : eliminarFACT,
        postearFACT : postearFACT
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('ListadoFacturasCtrl', ['$scope', '$filter', '$rootScope', '$timeout', '$window', 'appService', 'FacturacionService', 'InventarioService', 'ContabilidadService', 
                                        function ($scope, $filter, $rootScope, $timeout, $window, appService, FacturacionService, InventarioService, ContabilidadService) {
      
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

      //Traer todos los socios a javascript
      FacturacionService.socios().then(function (data) {
        $scope.todosLosSocios = data;
      });

      //Traer los documentos de posibles posteos: AL CONTADO --- A CREDITO
      appService.getDocumentoCuentas('FACT').then(function (data) {
        $scope.documentoCuentasFACT = data;
      });

      appService.getDocumentoCuentas('FACC').then(function (data) {
        $scope.documentoCuentasFACC = data;
      });          

      // Mostrar/Ocultar panel de Listado de Facturas
      $scope.toggleLF = function() {
        $scope.showLF = !$scope.showLF;

        if($scope.showLF === true) {
          $scope.ArrowLF = 'UpArrow';
        } else {
          $scope.ArrowLF = 'DownArrow';
        }
      }

      // Mostrar/Ocultar posteo Contabilidad
      $scope.toggleInfo = function() {
        $scope.showPostear = !$scope.showPostear;
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

            if(isNaN(data)) {
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

      //Eliminar Factura (Borra el detalle de EXISTENCIA y pone estatus BORRADO, pero el registro sigue en base de datos)
      $scope.eliminarFactura = function($event) {
        $event.preventDefault();

        try {
          FacturacionService.eliminarFACT($scope.dataH.factura).then(function (data) {
            if(data == 1) {
              $scope.errorShow = false;
              $scope.listadoFacturas();
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

      // Visualizar Documento (Factura Existente - desglose)
      $scope.FactFullById = function(NoFact, usuario) {
        try {

          FacturacionService.DocumentoById(NoFact).then(function (data) {

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
        $scope.facturasSeleccionadas = [];

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
          $scope.facturasSeleccionadas = _.without($scope.facturasSeleccionadas, _.findWhere($scope.facturasSeleccionadas, {id : iReg.id}));
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

      //Traer Socios
      $scope.getSocio = function($event) {
        $event.preventDefault();

        $scope.tableSocio = true;

        if($scope.socioNombre != undefined) {
          $scope.socios = $scope.todosLosSocios.filter(function (registro) {
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
        } else {
          $scope.socios = $scope.todosLosSocios;
          $scope.socioCodigo = '';
        }
      }

      //Agregar Producto
      $scope.addProducto = function($event, Prod) {
        $event.preventDefault();
        $scope.errorShow = false;

        try {

          //Debe seleccionar un almacen.
          if ($scope.dataH.almacen == undefined || $scope.dataH.almacen == '') {
            $scope.mostrarError('Debe seleccionar un almacen');
            throw "Debe seleccionar un almacen";
          }

          //No agregar el producto si ya existe
          $scope.dataD.forEach(function (item) {
            if(item.codigo == Prod.codigo) {
              $scope.mostrarError("No puede agregar mas de una vez el producto : " + item.descripcion);
              throw "No puede agregar mas de una vez el producto : " + item.descripcion;
            }
          });


          var existencia = 0;

          InventarioService.getExistenciaByProducto(Prod.codigo, $scope.dataH.almacen).then(function (data) {

            if(data.length > 0) {
              existencia = data[0]['cantidad'];

              //Si en algun momento existe un producto con disponibilidad en negativo no puede permitir agregarlo.
              if(existencia <= 0) {
                $scope.mostrarError('No hay disponibilidad para el producto : ' + Prod.descripcion);
                throw 'No hay disponibilidad para el producto : ' + Prod.descripcion;
              }

              if(existencia < 11 && existencia > 0) {
                $scope.mostrarError('El producto ' + Prod.descripcion + ' tiene una existencia de ' + data[0]['cantidad']);
              }

              Prod.descuento = 0;
              Prod.cantidad = 1;
              Prod.existencia = existencia;

              $scope.dataD.push(Prod);
              $scope.tableProducto = false;

              $scope.calculaTotales();

            } else {
              $scope.mostrarError('Este producto (' + Prod.descripcion + ') no tiene existencia.');
              throw 'Este producto (' + Prod.descripcion + ') no tiene existencia.';
            }
          });
        } catch(e) {
          $scope.mostrarError(e);
        }

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
          var total = 0.0;
          var subtotal = 0.0;
          var total_descuento = 0.0;
          var descuento = 0.0;

          if($scope.existError == true) {
            $scope.errorShow = false;
            $scope.existError = false;
          } 

          $scope.dataD.forEach(function (item) {
            if (item.descuento != undefined && item.descuento > 0) {
              descuento = parseFloat(item.descuento/100);
              descuento = (item.precio * descuento * item.cantidad);
            }

            //Verificar si la cantidad no excede la existencia disponible
            if(parseFloat(item.cantidad) > parseFloat(item.existencia)) {
              $scope.existError = true;
              $scope.mostrarError('No puede digitar una cantidad mayor a la disponibilidad : ' + item.existencia);
              throw 'No puede digitar una cantidad mayor a la disponibilidad : ' + item.existencia;
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
          $scope.totalDebitoCredito();
        }
      }

      //Funcion para postear los registros seleccionados. (Postear es llevar al Diario)
      $scope.postear = function(){
        var idoc = 0;
        $scope.iDocumentos = 0;

        $scope.showPostear = true;
        $scope.desgloseCuentas = [];

        $scope.posteoG = false;

        try {

          //Prepara cada linea de posteo
          $scope.facturasSeleccionadas.forEach(function (item) {
            if(item.terminos == 'CR') {
              $scope.documentoCuentas = $scope.documentoCuentasFACC;
            } else {
              $scope.documentoCuentas = $scope.documentoCuentasFACT;
            }

            $scope.documentoCuentas.forEach(function (documento) {
              var desgloseCuenta = new Object();
              
              console.log('Documento de Cuentas:');
              console.log(documento);
              console.log('Documento de Factura:');
              console.log(item);

              if(documento.getTipoSocio == 'N' || documento.getTipoSocio == item.tipoSocio) {
                desgloseCuenta.cuenta = documento.getCuentaCodigo;
                desgloseCuenta.descripcion = documento.getCuentaDescrp;
                desgloseCuenta.ref = documento.getCodigo + item.noFactura;
                desgloseCuenta.debito = documento.accion == 'D'? item.totalGeneral.toString().replace('$','') : $filter('number')(0.00, 2);
                desgloseCuenta.credito = documento.accion == 'C'? item.totalGeneral.toString().replace('$','') : $filter('number')(0.00, 2);

                $scope.desgloseCuentas.push(desgloseCuenta);
              }
            });

            idoc += 1;
            $scope.totalDebitoCredito();
            console.log($scope.desgloseCuentas);

          });

          $scope.iDocumentos = idoc;
        

        } catch(e) {
          alert(e);
        }
      }

      //Este metodo escribe en el diario general los registros correspondientes al desglose de cuenta
      //para este modulo de Facturacion.
      $scope.postearContabilidad = function() {

        try {

          //Validar que el CREDITO cuadre con el DEBITO
          if($scope.totalDebito != $scope.totalCredito && $scope.totalDebito > 0) {
            throw "El valor TOTAL del DEBITO es distinto al valor TOTAL del CREDITO.";
          }

          $scope.posteoG = true;
          $scope.desgloseCuentas.forEach(function (item) {
            ContabilidadService.guardarEnDiario(Date.now(), item.cuenta, item.ref, item.debito, item.credito).then(function (data) {
              console.log('Registros guardados en el diario');
              console.log(data);
            });
          });

          FacturacionService.postearFACT($scope.facturasSeleccionadas).then(function (data) {
            console.log(data);
            $scope.listadoFacturas();
          });

          alert('Los registros fueron posteados con exito!');

        } catch (e) {
          alert(e);
        }
      } //Linea FIN de posteo Contabilidad.

      //Sumarizar el total de CREDITO y total de DEBITO antes de postear (llevar a contabilidad).
      $scope.totalDebitoCredito = function() {
        $scope.totalDebito = 0.00;
        $scope.totalCredito = 0.00;

        $scope.desgloseCuentas.forEach(function (documento) {
          $scope.totalDebito += parseFloat(documento.debito.replaceAll(',',''));
          $scope.totalCredito += parseFloat(documento.credito.replaceAll(',',''));
        });
      }

      //Imprimir factura
      $scope.ImprimirFactura = function(factura) {
        $window.sessionStorage['factura'] = JSON.stringify(factura);
        $window.open('/facturacion/print/{factura}'.replace('{factura}',factura.noFactura), target='_blank'); 
      }

    }])

   //*************************************************//
   // CONTROLLERS  ORDEN DE SUPERCOOP                *
   //*************************************************//
   .controller('OrdenSuperCoopCtrl', ['$scope', '$filter', '$rootScope', 'SolicitudOrdenDespachoService', 'FacturacionService',
                                      function ($scope, $filter, $rootScope, SolicitudOrdenDespachoService, FacturacionService) {
    
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

          // $scope.OC.oficial = oficial;
          $scope.OC.categoriaId = data[0]['id'];
          $scope.OC.categoriaDescrp = data[0]['descripcion'];
          $scope.OC.interesA = data[0]['interesAnualSocio'];
          $scope.OC.interesM = parseFloat(data[0]['interesAnualSocio'])/12;
          $scope.OC.cantidadCuotas = 2;
          $scope.OC.valorCuotas = $filter('number')(parseFloat($rootScope.total.replace(',','')) /2, 2);

        });
      }

      //Guardar Orden de Compra SUPERCOOP
      $rootScope.guardarOrden = function($event) {
        $event.preventDefault();

        try {
          var Orden = new Object();
          Orden.solicitud = {};
          Orden.solicitante = {};

          Orden.fechaSolicitud = $filter('date')(Date.now(),'yyyy-MM-dd');
          Orden.fechaDescuento = $filter('date')(Date.now(),'yyyy-MM-dd');

          Orden.solicitante.codigoEmpleado = $scope.socioCodigo;
          Orden.solicitante.cobrador = $scope.dataH.vendedor;
          Orden.solicitante.autorizador = $scope.dataH.vendedor;
          Orden.solicitante.representanteCodigo = 0;

          Orden.solicitud.solicitudNo = $scope.OC.solicitud != undefined? parseInt('0' + $scope.OC.solicitud) : 0;
          Orden.solicitud.categoriaPrestamoId = $scope.OC.categoriaId;
          Orden.solicitud.idSuplidor = -1;
          Orden.solicitud.montoSolicitado = $scope.total.toString();
          Orden.solicitud.netoDesembolsar = $scope.total.toString();
          Orden.solicitud.ahorrosCapitalizados = '0';
          Orden.solicitud.deudasPrestamos = '0';
          Orden.solicitud.prestacionesLaborales = '0';
          Orden.solicitud.valorGarantizado = '0';
          Orden.solicitud.nota = 'Orden realizada por facturacion';
          Orden.solicitud.tasaInteresAnual = 0;
          Orden.solicitud.tasaInteresMensual = 0;
          Orden.solicitud.cantidadCuotas = 2;
          Orden.solicitud.valorCuotas = $filter('number')(parseFloat($rootScope.total.replace(',','')) /2, 2).replace(',','');
          Orden.solicitud.factura = $rootScope.factura;

          SolicitudOrdenDespachoService.guardaSolicitudOD(Orden.solicitante, Orden.solicitud, Orden.fechaSolicitud, Orden.fechaDescuento).then(function (data) {
            if(data > 0) {
              $scope.OC.solicitud = $filter('numberFixedLen')(data, 8)
              
              $scope.disableOC = true;
              $scope.BotonOC = 'Boton-disabled';

              //Prepara productos para formato de Orden de Despacho
              var articulo = {};
              var articulos = [];

              $scope.dataD.forEach(function (item) {
                articulo = new Object();
                articulo.articulo = item.codigo + '-' + item.descripcion;
                articulo.cantidad = item.cantidad;
                articulo.descuento = item.descuento;
                articulo.precio = item.precio;

                articulos.push(articulo);
              });

              //Agregar Detalle a la Orden
              SolicitudOrdenDespachoService.guardaSolicitudODDetalle(data, articulos).then(function (data) {
                if(data == 1) {
                  notie.alert(1, 'Se guardó perfectamente!', 3);
                } else {
                  $scope.mostrarError(data);
                }
              });
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
          $scope.OC.autorizador = ordenD['autorizador'];
          $scope.OC.representante = ordenD['representante'];
          $scope.OC.interesA = ordenD['tasaInteresAnual'];
          $scope.OC.interesM = ordenD['tasaInteresMensual']
          $scope.OC.cantidadCuotas = ordenD['cuotas'];
          $scope.OC.valorCuotas = $filter('number')(ordenD['valorCuotas'], 2);

          $rootScope.oid = $scope.OC.solicitud;

        } catch (e) {
          $rootScope.mostrarError(e);
        }
      }
    }])  


  //****************************************************
  //CONTROLLERS PRINT DOCUMENT                         *
  //****************************************************
  .controller('ImprimirFacturaCtrl', ['$scope', '$filter', '$window', 'FacturacionService', function ($scope, $filter, $window, FacturacionService) {
    $scope.factura = JSON.parse($window.sessionStorage['factura']);
    $scope.dataH = {};
    $scope.dataD = [];

    FacturacionService.DocumentoById($scope.factura.noFactura).then(function (data) {

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

    $scope.imprimirFact = function() {

      FacturacionService.impresionFact($scope.factura.noFactura).then(function (data) {
        console.log("DATA: " + data);

        document.getElementById('printBoton').style.display = "None";
        window.print();
        window.location.reload();
        document.getElementById('printBoton').style.display = "";
      });
      // var doc = jsPDF();
      // doc.text(20,20, 'HOLA MUDO');
      // doc.save('pruebaPDF.pdf');
      // console.log(doc);
    }

    $scope.totalValor = function() {
      var total = 0.0;
      var descuento = 0;

      $scope.dataD.forEach(function (item) {
        if(parseFloat(item.descuento) > 0) {
          descuento = (parseFloat(item.descuento)/100);
          descuento = (parseFloat(item.precio) * parseFloat(descuento) * parseFloat(item.cantidad));
        } else {
          descuento = 0;
        }
        total += (parseFloat(item.precio) * parseFloat(item.cantidad)) - descuento;
      });

      return total;
    }

    $scope.totalDescuento = function() {
      var total = 0.0;
      var descuento = 0.0;

      $scope.dataD.forEach(function (item) {
        if(parseFloat(item.descuento) > 0) {
          descuento = (parseFloat(item.descuento)/100);
          descuento = (parseFloat(item.precio) * parseFloat(descuento) * parseFloat(item.cantidad));
        } else {
          descuento = 0;
        }
        total += descuento;
      });

      return total;
    }

    $scope.hora = function() {
      return Date.now();
    }

  }])

  //****************************************************
  //CONTROLLERS Reporte Utilidades                     *
  //****************************************************
  .controller('ImprimirReporteUtilidadCtrl', ['$scope', '$filter', 'FacturacionService',
                                              function ($scope, $filter, FacturacionService) {

    // Inicializacion de Variables


    // Funcion para mostrar error por pantalla
    $scope.mostrarError = function(error) {
      $scope.errorMsg = error;
      $scope.errorShow = true;
    }

    // Mostrar/Ocultar error
    $scope.toggleError = function() {
      $scope.errorShow = !$scope.errorShow;
    }

    // Para imprimir reporte de Utilidades
    $scope.reporteUtilidades = function() {
      try {
        var fechaInicio = $scope.fechaInicio.split('/');
        var fechaI = fechaInicio[2] + '-' + fechaInicio[1] + '-' + fechaInicio[0];

        var fechaFin = $scope.fechaFin.split('/');
        var fechaF = fechaFin[2] + '-' + fechaFin[1] + '-' + fechaFin[0];

        $scope.totalCantidad_ = 0;
        $scope.totalPrecio_ = 0;
        $scope.totalCosto_ = 0;
        $scope.totalPorcentajeCosto_ = 0;
        $scope.totalMargen_ = 0;
        $scope.totalPorcentajeMargen_ = 0;

        FacturacionService.reporteUtilidad().then(function (data) {
          $scope.registros = data.filter(function (item) {
            return $filter('date')(item.fecha, 'yyyy-MM-dd') >= fechaI && $filter('date')(item.fecha,'yyyy-MM-dd') <= fechaF;
          });

          $scope.registros.forEach(function (item) {
            $scope.totalCantidad_ += parseFloat(item.cantidad);
            $scope.totalPrecio_ += parseFloat(item.precio);
            $scope.totalCosto_ += parseFloat(item.costo);
            $scope.totalPorcentajeCosto_ += parseFloat((item.costo/item.precio) * 100);
            $scope.totalMargen_ += parseFloat(item.margen);
            $scope.totalPorcentajeMargen_ += parseFloat((item.margen/item.costo) * 100)

          })
        });

      } catch (e) {
        $scope.mostrarError(e);
      }
    }

  }])

  //****************************************************
  //CONTROLLERS Reporte de Ventas Diarias              *
  //****************************************************
  .controller('RPTVentasDiariasCtrl', ['$scope', '$filter', 'FacturacionService',
                                              function ($scope, $filter, FacturacionService) {

    // Inicializacion de Variables


    // Funcion para mostrar error por pantalla
    $scope.mostrarError = function(error) {
      $scope.errorMsg = error;
      $scope.errorShow = true;
    }

    // Mostrar/Ocultar error
    $scope.toggleError = function() {
      $scope.errorShow = !$scope.errorShow;
    }

    // Para imprimir reporte de Ventas Diarias
    $scope.ventasDiarias = function() {
      try {
        var fechaInicio = $scope.fechaInicio.split('/');
        var fechaI = fechaInicio[2] + '-' + fechaInicio[1] + '-' + fechaInicio[0];

        var fechaFin = $scope.fechaFin.split('/');
        var fechaF = fechaFin[2] + '-' + fechaFin[1] + '-' + fechaFin[0];

        FacturacionService.all().then(function (data) {
          $scope.registros = data.filter(function (item) {
            console.log($filter('date')(item.fecha, 'yyyy-MM-dd'))
            console.log(fechaI)
            return $filter('date')(item.fecha, 'yyyy-MM-dd') >= fechaI && $filter('date')(item.fecha,'yyyy-MM-dd') <= fechaF;
          });

          $scope.totales();

        });
      } catch (e) {
        $scope.mostrarError(e);
      }
    }

    // Total de monto en Credito
    $scope.totales = function() {
      $scope.totalCredito = 0;
      $scope.totalContado = 0;

      $scope.registros.forEach(function (item) {
        if(item.terminos == 'CR') {
          $scope.totalCredito += parseFloat(item.totalGeneral.replace('$','').replace(',',''));
          console.log($scope.totalCredito)
          console.log(item.totalGeneral)
        } else {
          $scope.totalContado += parseFloat(item.totalGeneral.replace('$','').replace(',',''));
        }
      });
    }

  }])

  //****************************************************
  //CONTROLLERS Reporte de Resumen de Ventas           *
  //****************************************************
  .controller('RPTVentasResumidoCtrl', ['$scope', '$filter', 'FacturacionService',
                                              function ($scope, $filter, FacturacionService) {

    // Inicializacion de Variables


    // Funcion para mostrar error por pantalla
    $scope.mostrarError = function(error) {
      $scope.errorMsg = error;
      $scope.errorShow = true;
    }

    // Mostrar/Ocultar error
    $scope.toggleError = function() {
      $scope.errorShow = !$scope.errorShow;
    }

    // Para imprimir reporte de Resumen de Ventas
    $scope.ventasResumido = function() {
      try {
        var fechaInicio = $scope.fechaInicio.split('/');
        var fechaI = fechaInicio[2] + '-' + fechaInicio[1] + '-' + fechaInicio[0];

        var fechaFin = $scope.fechaFin.split('/');
        var fechaF = fechaFin[2] + '-' + fechaFin[1] + '-' + fechaFin[0];

        FacturacionService.resumenVentas(fechaI, fechaF).then(function (data) {
          $scope.registros = data;
          $scope.totalesValores();

        });
      } catch (e) {
        $scope.mostrarError(e);
      }
    }

    // Total de monto en Credito
    $scope.totalesValores = function() {
      $scope.totalValor = 0;

      $scope.registros.forEach(function (item) {
        $scope.totalValor += item.valor;
      });
    }

  }]);
   
})(_);