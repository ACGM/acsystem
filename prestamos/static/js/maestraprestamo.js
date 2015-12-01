(function (_) {

  angular.module('cooperativa.maestraprestamo', ['ngAnimate'])

    // Filtro para manejo de bloqueo de seleccion de prestamo segun el estatus (checkbox)
    .filter('posteoMP', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('E', false)
                .replace('D', false)
                .replace('C', false)
                .replace('P', true)
                .replace('S', true);
        return input;
      }
    })

    // Filtro para imagenes a mostrar por cada estatus del prestamo.
    .filter('OpenCloseMP', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('E', 'icon-folder-open')
                .replace('P', 'icon-folder')
                .replace('S', 'icon-folder')
                .replace('C', 'icon-banknote')
                .replace('D', 'icon-coin');
        return input;
      }
    })

    .factory('MaestraPrestamoService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Cambios Prestamo
      function guardarCambios(prestamo) {
        var deferred = $q.defer();

        $http.post('/prestamos/maestra/cambios/', JSON.stringify({'noPrestamo': prestamo.noPrestamo,
                                                                  'tipoNomina': prestamo.tipoNomina,
                                                                  'montoQ1': prestamo.montoQ1,
                                                                  'montoQ2': prestamo.montoQ2})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Llenar el listado de prestamos
      function all() {
        var deferred = $q.defer();

        $http.get('/api/prestamos/maestra/listado/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Marcar Prestamo como Desembolso Electronico o Cheque.
      function MarcarPrestamoDC(prestamos, accion) {
        var deferred = $q.defer();
        console.log(prestamos);

        $http.post('/prestamos/maestra/marcarcomo/', JSON.stringify({'prestamos': prestamos, 'accion': accion})). 
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un prestamo en especifico (Desglose)
      function PrestamoById(NoPrestamo) {
        var deferred = $q.defer();
        var doc = NoPrestamo != undefined? NoPrestamo : 0;

        $http.get('/maestraPrestamojson/?noprestamo={NoPrestamo}&format=json'.replace('{NoPrestamo}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar un numero de prestamo en especifico en listado de prestamos
      function byNoPrestamo(NoPrestamo) {
        var deferred = $q.defer();
        all().then(function (data) {
          var result = data.filter(function (documento) {
            return documento.noPrestamo == NoPrestamo;
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }

      //Buscar Prestamos por socio
      function PrestamosbySocio(codigoSocio){
        var deferred = $q.defer();

        all().then(function (data) {
          var results = data.filter(function (registros) {
            return registros.codigoSocio == codigoSocio;
          });

          if(results.length > 0) {
            deferred.resolve(results);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }

      // Marcar prestamos como posteados.
      function PostearPrestamosOD(prestamos) {
        var deferred = $q.defer();

        $http.post('/maestraPrestamos/prestamosOD/postear/', JSON.stringify({'prestamos': prestamos})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Prestamos/OD posteados.
      function PrestamosPosteados() {
        var deferred = $q.defer();
        all().then(function (data) {
          var result = data.filter(function (documento) {
            return documento.estatus == 'P';
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }

      //Buscar los prestamos de un socio (prestamos aprobados)
      function prestamosDetalleByCodigoSocio(socio) {
        var deferred = $q.defer();

        $http.get('/api/prestamos/maestra/socio/detalle/{socio}/?format=json'.replace('{socio}', socio))
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Buscar los balances de prestamos de un socio (undefined = todos)
      function prestamosBalanceByCodigoSocio(socio) {
        var deferred = $q.defer();

        if(socio == undefined) {
          url = '/api/prestamos/maestra/socio/balance/?format=json';
        } else {
          url = '/api/prestamos/maestra/socio/balance/{socio}/?format=json'.replace('{socio}', socio);
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Pagos Cuotas de Prestamos
      function PagoCuotasPrestamosByNoPrestamo(NoPrestamo) {
        var deferred = $q.defer();

        if(NoPrestamo != undefined) {
          url = '/prestamos/pago-cuotas/{NoPrestamo}/?format=json'.replace('{NoPrestamo}', NoPrestamo);
        } else {
          url = '/prestamos/pago-cuotas/?format=json';
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Reporte de Prestamos
      function ReportePrestamos(fechaI, fechaF, estatus, agrupar) {
        var deferred = $q.defer();

        if(agrupar == false) {
          url = '/prestamos/reportes/consultaPrestamos/{fechaI}/{fechaF}/{estatus}/?format=json'.replace('{fechaI}', fechaI)
                                                                                                .replace('{fechaF}', fechaF)
                                                                                                .replace('{estatus}', estatus);
        } else {
          url = '/prestamos/reportes/consultaPrestamos/agrupadosPorCategoria/?fechaI={fechaI}&fechaF={fechaF}&estatus={estatus}'
                                                                                              .replace('{fechaI}', fechaI)
                                                                                              .replace('{fechaF}', fechaF)
                                                                                              .replace('{estatus}', estatus);
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Estado de Cuenta Socio
      function EstadoCuentaBySocio(codigo) {
        var deferred = $q.defer();

        url = '/estadoCuentajson/?codigo={codigo}'.replace('{codigo}', codigo);
        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      return {
        all: all,
        byNoPrestamo                    : byNoPrestamo,
        PrestamosbySocio                : PrestamosbySocio,
        PrestamoById                    : PrestamoById,
        MarcarPrestamoDC                : MarcarPrestamoDC,
        PostearPrestamosOD              : PostearPrestamosOD,
        PrestamosPosteados              : PrestamosPosteados,
        guardarCambios                  : guardarCambios,
        prestamosDetalleByCodigoSocio   : prestamosDetalleByCodigoSocio,
        prestamosBalanceByCodigoSocio   : prestamosBalanceByCodigoSocio,
        PagoCuotasPrestamosByNoPrestamo : PagoCuotasPrestamosByNoPrestamo,
        ReportePrestamos                : ReportePrestamos,
        EstadoCuentaBySocio             : EstadoCuentaBySocio
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('MaestraPrestamosCtrl', ['$scope', '$filter', '$timeout', '$window', 'MaestraPrestamoService', 'appService', 'ContabilidadService',
                                        function ($scope, $filter, $timeout, $window, MaestraPrestamoService, appService, ContabilidadService) {
      
      //Inicializacion de variables
      $scope.disabledButton = 'Boton-disabled';
      $scope.disabledButtonBool = true;
      $scope.errorShow = false;
      $scope.showLP = true;
      $scope.regAll = false;

      $scope.prestamosSeleccionados = [];
      $scope.reg = [];
      $scope.valoresChk = [];
      $scope.dataH = {};
      $scope.prestamo = {};

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLP = 'UpArrow';

      panelesSize();

      window.onresize = function(event) {
        panelesSize();
      }

      function panelesSize() {
        document.getElementById('prestamosContainer').style.height = (window.innerHeight - 220) + 'px';
      }

      // Mostrar/Ocultar panel de Listado de Facturas
      $scope.toggleLP = function() {
        $scope.showLP = !$scope.showLP;

        if($scope.showLP === true) {
          $scope.ArrowLP = 'UpArrow';
        } else {
          $scope.ArrowLP = 'DownArrow';
        }
      }

      // Mostrar/Ocultar posteo Contabilidad
      $scope.toggleInfo = function() {
        $scope.showPostear = !$scope.showPostear;
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

      //Listado de todos los prestamos
      $scope.listadoPrestamos = function() {
        $scope.NoFoundDoc = '';
        $scope.prestamosSeleccionados = [];
        $scope.valoresChk = [];

        MaestraPrestamoService.all().then(function (data) {
          $scope.prestamos = data;
          
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

      //Ordenar por Socio
      $scope.ordenarPorSocio = function($event) {
        $scope.prestamos.sort(function(a,b) {
          if(a.socio > b.socio) {
            return 1;
          }
          if(a.socio < b.socio) {
            return -1;
          }
          return 0;
        });
      }

      //Ordenar por Categoria de Prestamo
      $scope.ordenarPorCategoria = function($event) {
        $scope.prestamos.sort(function(a,b) {
          if(a.categoriaPrestamo > b.categoriaPrestamo) {
            return 1;
          }
          if(a.categoriaPrestamo < b.categoriaPrestamo) {
            return -1;
          }
          return 0;
        });
      }

      //Guardar Cambios en Prestamo Seleccionado.
      $scope.GuardarCambiosPrestamo = function($event) {
        var prestamo = {};

        prestamo.noPrestamo = $scope.dataH.noPrestamo;
        prestamo.tipoNomina = $scope.dataH.tipoPrestamoNomina;
        prestamo.montoQ1 = $scope.prestamo.montoCuotaQ1;
        prestamo.montoQ2 = $scope.prestamo.montoCuotaQ2;

        MaestraPrestamoService.guardarCambios(prestamo).then(function (data) {
          if(data == 1) {
            $scope.PrestamoFullById($event, $scope.dataH.noPrestamo);
            alert('Los cambios fueron guardados.');
          } else {
            $scope.mostrarError(data);
          }
        })

      }

      //Buscar un prestamo en especifico
      $scope.filtrarPorNoPrestamo = function(NoPrestamo) {
        try {
          MaestraPrestamoService.byNoPrestamo(NoPrestamo).then(function (data) {
            $scope.prestamos = data;

            if(data.length > 0) {
              $scope.verTodos = '';
              $scope.NoFoundDoc = '';
            }
          }, 
            (function () {
              $scope.NoFoundDoc = 'No se encontró el prestamo #' + NoPrestamo;
            }
          ));          
        } catch (e) {
          console.log(e);
        }
      }

      //Buscar Documento por ENTER
      $scope.buscarPrestamo = function($event, NoPrestamo) {
        if($event.keyCode == 13) {
          $scope.filtrarPorNoPrestamo(NoPrestamo);
        }
      }

      //Buscar prestamos en especifico por socio
      $scope.filtrarPorSocio = function(codigoSocio) {
        try {
          MaestraPrestamoService.PrestamosbySocio(codigoSocio).then(function (data) {
            $scope.prestamos = data;

            if(data.length > 0) {
              $scope.verTodos = '';
              $scope.NoFoundDoc = '';
            }
          }, 
            (function () {
              $scope.NoFoundDoc = 'No se encontró prestamo para el socio: ' + codigoSocio;
            }
          ));          
        } catch (e) {
          console.log(e);
        }
      }

      //Buscar Documento por ENTER (by Socio)
      $scope.buscarPrestamoBySocio = function($event, codigoSocio) {
        if($event.keyCode == 13) {
          $scope.filtrarPorSocio(codigoSocio);
        }
      }


      // Visualizar Prestamo (desglose)
      $scope.PrestamoFullById = function($event, prestamo) {
        $event.preventDefault();

        try {
          MaestraPrestamoService.PrestamoById(prestamo).then(function (data) {
            if(data.length > 0) {
              $scope.errorMsg = '';
              $scope.errorShow = false;
              console.log(data);

              //completar los campos
              // $scope.nuevaEntrada();

              var solicitudNo = data[0]['noSolicitudPrestamo'] == ''? data[0]['noSolicitudOD'] : data[0]['noSolicitudPrestamo'];

              $scope.dataH.noPrestamo = $filter('numberFixedLen')(data[0]['noPrestamo'],9);
              $scope.dataH.factura = data[0]['factura'];
              $scope.dataH.categoriaPrestamoDescrp = data[0]['categoriaPrestamoDescrp'];
              $scope.dataH.representanteCod = data[0]['representanteCodigo'];
              $scope.dataH.representanteDescrp = data[0]['representanteNombre'];
              $scope.dataH.socioCodigo = data[0]['socioCodigo'];
              $scope.dataH.socioNombre = data[0]['socioNombre'];
              $scope.dataH.socioCedula = data[0]['socioCedula'];
              $scope.dataH.socioDepartamento = data[0]['socioDepartamento'];
              $scope.dataH.oficial = data[0]['oficial'];
              $scope.dataH.localidad = data[0]['localidad'];
              $scope.dataH.estatus = data[0]['estatus'];
              $scope.dataH.posteadoFecha = data[0]['posteadoFecha'];
              $scope.dataH.tipoPrestamoNomina = data[0]['tipoPrestamoNomina'];

              $scope.prestamo.documentoDescrp = data[0]['documentoDescrp'];
              $scope.prestamo.noSolicitud = $filter('numberFixedLen')(solicitudNo, 8);
              $scope.prestamo.monto = $filter('number')(data[0]['montoInicial'], 2);
              $scope.prestamo.tasaInteresAnual = data[0]['tasaInteresAnual'];
              $scope.prestamo.tasaInteresMensual = data[0]['tasaInteresMensual']/2;
              $scope.prestamo.tasaInteresPrestBaseAhorro = data[0]['tasaInteresPrestBaseAhorro']/2;
              $scope.prestamo.pagoPrestamoAnterior = data[0]['pagoPrestamoAnterior'];
              $scope.prestamo.cantidadCuotas = data[0]['cantidadCuotas'];
              $scope.prestamo.montoCuotaQ1 = $filter('number')(data[0]['montoCuotaQ1'], 2);
              $scope.prestamo.montoCuotaQ2 = $filter('number')(data[0]['montoCuotaQ2'], 2);
              $scope.prestamo.fechaDesembolso = data[0]['fechaDesembolso'];
              $scope.prestamo.fechaEntrega = data[0]['fechaEntrega'];
              $scope.prestamo.chequeNo = data[0]['chequeNo'];
              $scope.prestamo.valorGarantizado = $filter('number')(data[0]['valorGarantizado'], 2);
              $scope.prestamo.valorAhorro = $filter('number')(data[0]['valorAhorro'], 2);
              $scope.prestamo.balance = $filter('number')(data[0]['balance'], 2);

              $scope.prestamo.valorInteresGarantizado = $filter('number')(data[0]['valorGarantizado'] * (data[0]['tasaInteresMensual']/data[0]['quincenas']/100), 2);
              $scope.prestamo.valorInteresAhorro = $filter('number')(data[0]['valorAhorro'] * (data[0]['tasaInteresPrestBaseAhorro']/data[0]['quincenas']/100), 2)

              var fechaP = $filter('date')(Date.now(), 'dd/MM/yyyy').split('/');
              var fechaF = new Date(fechaP[2] + '/' + fechaP[1] + '/' + fechaP[0]);

              var nextDate = new Date();
              nextDate.setDate(fechaF.getDate()+parseInt($scope.prestamo.cantidadCuotas * 15));

              $scope.prestamo.fechaVencimiento = $filter('date')(nextDate, 'dd/MM/yyyy');


              // if(data[0]['estatus'] == 'P') {
              //   $scope.disabledButton = 'Boton';
              //   $scope.disabledButtonBool = false;
              // } else {
              //   $scope.disabledButton = 'Boton-disabled';
              //   $scope.disabledButtonBool = true;
              // }

            }

          }, 
            (function () {
              $scope.mostrarError('No pudo encontrar el desglose del prestamo #' + prestamo);
            }
          ));
        }
        catch (e) {
          $scope.mostrarError(e);
        }

        if($scope.showLP == true) {
          $scope.toggleLP();
        }
      }

      //Marcar Prestamo como Cheque
      $scope.marcarPrestamoDC = function(prestamo, accion) {
        var p = [];
        p.push(prestamo);

        MaestraPrestamoService.MarcarPrestamoDC(p, accion).then(function (data) {
          if(data == 1) {
            $scope.listadoPrestamos();
          } else {
            $scope.mostrarError(data);
          }
        }, function() {
          $scope.mostrarError("Hubo un error interno en la aplicacion, contacte al administrador.");
        })
      }

      
      //Funcion para postear los registros seleccionados. (Postear es llevar al Diario)
      $scope.postear = function($event, prestamo){
        var idoc = 0;
        $scope.iDocumentos = 0;

        $scope.showPostear = true;
        $scope.desgloseCuentas = [];
        $scope.posteoG = false;

        try {
          
          console.log(prestamo);

          //Verificar si es un Prestamo o una Orden de Despacho.
          if(prestamo.documentoDescrp == 'Prestamo') {
            docCuentas = 'PRES';
          } else {
            if(prestamo.getRNCSuplidor == '11111111111') {
              docCuentas = 'ORD2';
            } else {
              docCuentas = 'ORD1';
            }
          }

          $scope.prestamoOD_SEL = prestamo; //Asigno el prestamo para cuando se vaya a "Llevar a Contabilidad"

          appService.getDocumentoCuentas(docCuentas).then(function (data) {
            $scope.documentoCuentas = data;
    
            //Prepara cada linea de posteo
            $scope.documentoCuentas.forEach(function (documento) {
              var desgloseCuenta = new Object();

              console.log('Documento de Cuentas:');
              console.log(documento);
              console.log('Documento de Prestamo:');
              console.log($scope.prestamoOD_SEL);

              if(documento.getTipoSocio == 'N' || documento.getTipoSocio == $scope.prestamoOD_SEL.tipoSocio) {
                valor = 0;

                //Para cuando es una PRETAMO
                if($scope.prestamoOD_SEL.documentoDescrp == 'Prestamo') {
                  valor = $filter('number') ($scope.prestamoOD_SEL.montoInicial, 2);

                } else { //Para las ORDENES DE DESPACHO
                  
                  if(documento.getCuentaCodigo == 410201) { //La cuenta de FINANCIAMIENTO 410201
                    valor = $filter('number') ($scope.prestamoOD_SEL.getMontoInteres, 2);
                  }

                  if(documento.getCuentaCodigo == 21010401 || documento.getCuentaCodigo == 190101) { //Cuenta Proveedor/Sirena
                    valor = $filter('number') ($scope.prestamoOD_SEL.getMontoSinInteres, 2);
                  }

                  if(documento.getCuentaCodigo == 11130201 || documento.getCuentaCodigo == 11130202) { //Cuenta Socio/Empleado
                    valor = $filter('number') ($scope.prestamoOD_SEL.montoInicial, 2);
                  }
                }

                desgloseCuenta.cuenta = documento.getCuentaCodigo;
                desgloseCuenta.descripcion = documento.getCuentaDescrp;
                desgloseCuenta.ref = documento.getCodigo + $scope.prestamoOD_SEL.noPrestamo;
                desgloseCuenta.debito = documento.accion == 'D'? valor : $filter('number')(0.00, 2);
                desgloseCuenta.credito = documento.accion == 'C'? valor : $filter('number')(0.00, 2);

                $scope.desgloseCuentas.push(desgloseCuenta);
              }
              
            });
            $scope.totalDebitoCredito();     
            $scope.postearContabilidad();

          });
        } catch (e) {
          alert(e);
        }
      }

      //Este metodo escribe en el diario general los registros correspondientes al desglose de cuenta
      //para este modulo de Inventario - Salida.
      $scope.postearContabilidad = function() {

        try {

          //Validar que el CREDITO cuadre con el DEBITO
          if($scope.totalDebito != $scope.totalCredito && $scope.totalDebito > 0) {
            throw "El valor TOTAL del DEBITO es distinto al valor TOTAL del CREDITO.";
          }

          $scope.posteoG = true;
          $scope.desgloseCuentas.forEach(function (item) {
            console.log('Item a Postear: ');
            console.log(item)

            ContabilidadService.guardarEnDiario(Date.now(), item.cuenta, item.ref, item.debito, item.credito).then(function (data) {
              if(data.substring(0,1) == '-') {
                $scope.mostrarError(data);
              } else {
                console.log('Registros guardados en el diario: ' + data);
              }
            });
          });

          var p = [];
          p.push ($scope.prestamoOD_SEL);

          MaestraPrestamoService.PostearPrestamosOD(p).then(function (data) {
            if(data == 1) {
              // $scope.listadoPrestamos();
            } else {
              alert(data);
            }
          });

          $scope.toggleInfo();
          // alert('Los registros fueron posteados con exito!');

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

      //Para postear todos los prestamos -- Solo una vez (carga inicial)
      $scope.AllOneTime = function($event) {
        var allPrestamosPend = $scope.prestamos.filter(function (item) {
          return item.estatus != 'P';
        });

        allPrestamosPend.forEach(function (ite, index) {
          if (ite.estatus != 'P') {
            var run = setTimeout(function (msg) {
              console.log(ite);
              $scope.postear($event, ite);
            },index * 1000);
          }
        });
      }
      //Este metodo es para carga inicial.

    }])

    //****************************************************
    //REPORTE DE PRESTAMOS                               *
    //****************************************************
    .controller('ConsultarPrestamoCtrl', ['$scope', '$filter', '$timeout', '$window', 'MaestraPrestamoService', 'appService',
                                        function ($scope, $filter, $timeout, $window, MaestraPrestamoService, appService) {
      
      //Variables de Informacion General (EMPRESA)
      $scope.empresa = $window.sessionStorage['empresa'].toUpperCase();
      //Fin variables de Informacion General.
      
      //Inicializacion de variables
      $scope.agrupar = false;
      $scope.estatus = 'P';
      $scope.tipoSocio = 'S';

      //Funcion para buscar consulta de prestamos.
      $scope.buscarPrestamos = function($event) {
        try {
          var fechaInicio = $scope.fechaInicio.split('/');
          var fechaI = fechaInicio[2] + '-' + fechaInicio[1] + '-' + fechaInicio[0];

          var fechaFin = $scope.fechaFin.split('/');
          var fechaF = fechaFin[2] + '-' + fechaFin[1] + '-' + fechaFin[0];

          MaestraPrestamoService.ReportePrestamos(fechaI, fechaF, $scope.estatus, $scope.agrupar).then(function (data) {
            console.log(data);
            if($scope.agrupar == false) {
              $scope.registros = data.filter(function (item) {
                  return item.tipoSocio == $scope.tipoSocio;
              });
            } else {
              $scope.registros = data;
            }

            $scope.totales();
          });

        } catch (e) {
          alert(e);
        }
      }

      //Para prestamos agrupados por clasificacion se calcula el porcentaje de cada categoria
      $scope.porcentajesPrestamo = function() {
        var registros = $scope.registros;
        $scope.registros = [];
        $scope.registrosAgrupados = [];
        $scope.totalPorcentaje = 0;

        registros.forEach(function (item) {
          registro = {};
          registro.id = item.id;
          registro.categoriaPrestamo = item.categoriaPrestamo;
          registro.totalCantidad = item.totalCantidad;
          registro.totalMonto = item.totalMonto;
          registro.porcentaje = (item.totalMonto / $scope.totalMontoAgrupado) * 100;

          $scope.registrosAgrupados.push(registro);
          $scope.totalPorcentaje += registro.porcentaje;

        });
        console.log('LOS AGRUPADOS');
        console.log($scope.registrosAgrupados);
      }

      $scope.totales = function() {
        $scope.totalMontoOriginal = 0.00;
        $scope.totalBalance = 0.00;

        $scope.totalMontoAgrupado = 0.00;
        $scope.totalCantidadAgrupado = 0;

        $scope.registros.forEach(function (documento) {
          if($scope.agrupar != undefined) {
            $scope.totalMontoAgrupado += parseFloat(documento.totalMonto);
            $scope.totalCantidadAgrupado += parseFloat(documento.totalCantidad);

          } else {
            $scope.totalMontoOriginal += parseFloat(documento.montoInicial.replaceAll(',',''));
            $scope.totalBalance += parseFloat(documento.balance.replaceAll(',',''));
          }
        });

        if($scope.agrupar == true) {
          console.log('ENTRO A AGRUPAR')
          $scope.porcentajesPrestamo();
        }
      }
      
    }])

    //****************************************************
    //DISTRIBUCION DE INTERESES DE PRESTAMOS             *
    //****************************************************
    .controller('DistribucionInteresesPrestamosCtrl', ['$scope', '$filter', '$timeout', '$window', 'MaestraPrestamoService', 'appService',
                                        function ($scope, $filter, $timeout, $window, MaestraPrestamoService, appService) {
      
      //Variables de Informacion General (EMPRESA)
      $scope.empresa = $window.sessionStorage['empresa'].toUpperCase();
      //Fin variables de Informacion General.
      
      //Inicializacion de variables
      $scope.agrupar = false;

      //Funcion para buscar consulta de prestamos.
      $scope.buscarPrestamos = function($event) {
        try {
          var fechaInicio = $scope.fechaInicio.split('/');
          var fechaI = fechaInicio[2] + '-' + fechaInicio[1] + '-' + fechaInicio[0];

          var fechaFin = $scope.fechaFin.split('/');
          var fechaF = fechaFin[2] + '-' + fechaFin[1] + '-' + fechaFin[0];

          MaestraPrestamoService.ReportePrestamos(fechaI, fechaF, $scope.estatus, $scope.agrupar).then(function (data) {
            console.log(data);
            $scope.registros = data;

            $scope.totales();
          });

        } catch (e) {
          alert(e);
        }
      }

      $scope.VisualizarDistribucion = function() {
        alert('HOLA')
      }

      $scope.totales = function() {
        $scope.totalMontoOriginal = 0.00;
        $scope.totalBalance = 0.00;

        $scope.totalMontoAgrupado = 0.00;
        $scope.totalCantidadAgrupado = 0;

        $scope.registros.forEach(function (documento) {
          if($scope.agrupar != undefined) {
            $scope.totalMontoAgrupado += parseFloat(documento.totalMonto);
            $scope.totalCantidadAgrupado += parseFloat(documento.totalCantidad);

          } else {
            $scope.totalMontoOriginal += parseFloat(documento.montoInicial.replaceAll(',',''));
            $scope.totalBalance += parseFloat(documento.balance.replaceAll(',',''));
          }
        });

        if($scope.agrupar == true) {
          $scope.porcentajesPrestamo();
        }
      }
      
    }])

    //****************************************************
    //TABLA DE AMORTIZACION                              *
    //****************************************************
    .controller('TablaAmortizacionCtrl', ['$scope', '$filter', '$timeout', '$window', 'MaestraPrestamoService', 'appService',
                                        function ($scope, $filter, $timeout, $window, MaestraPrestamoService, appService) {
      

      $scope.calcularAmortizacion = function() {
        $scope.registros = [];
        var registro = {};

        //Primero tomamos los montos para el calculo
        var solicitar = $scope.ta.montoSolicitar;
        var ahorrado = $scope.ta.montoAhorrado;
        var garantia = $scope.ta.montoGarantizado;
        var capital = $scope.ta.montoSolicitar / $scope.ta.cantidadCuotas;
        var porcentajeCuotaAhorrado = ahorrado / solicitar;
        var porcentajeCuotaGarantizado = garantia / solicitar;
        var cuotaAh = capital * (porcentajeCuotaAhorrado/100);
        var cuotaGr = capital * (porcentajeCuotaGarantizado/100);

        var fecha = new Date();
        var IntAh = 0;
        var IntGr = 0;
        var balance = solicitar;

        if(garantia <=0) {
            ahorrado = solicitar;
        }

        var sumarDias = 15;

        for(i = 0; i<$scope.ta.cantidadCuotas; i++) {

          registro = {};

          var fecha = new Date();
          fecha.setDate(fecha.getDate()+sumarDias);

          registro.fecha = fecha;
          registro.capital = capital;
          registro.ahorrado = ahorrado;
          registro.garantia = garantia;

          //Calculo complejo de los intereses
          if(garantia <= 0) {
            registro.IA = balance * ($scope.ta.tasaInteresAhorrado/24/100);
            registro.IG = 0;

          } else {
            registro.IA = ahorrado * ($scope.ta.tasaInteresAhorrado/24/100);
            
            registro.IG = garantia * ($scope.ta.tasaInteresGarantizado/24/100);
            garantia -= registro.IG;
          }

          registro.totalInteres = registro.IA + registro.IG;

          registro.cuota = capital + registro.totalInteres;
          registro.balance = balance;
          
          $scope.registros.push(registro);

          balance = balance - capital
          ahorrado -= registro.IA;
          sumarDias += 15;
          
        }
        console.log($scope.registros);
      }

      $scope.totales = function() {
        $scope.totalMontoOriginal = 0.00;
        $scope.totalBalance = 0.00;

        $scope.totalMontoAgrupado = 0.00;
        $scope.totalCantidadAgrupado = 0;

        $scope.registros.forEach(function (documento) {
          if($scope.agrupar != undefined) {
            $scope.totalMontoAgrupado += parseFloat(documento.totalMonto);
            $scope.totalCantidadAgrupado += parseFloat(documento.totalCantidad);

          } else {
            $scope.totalMontoOriginal += parseFloat(documento.montoInicial.replaceAll(',',''));
            $scope.totalBalance += parseFloat(documento.balance.replaceAll(',',''));
          }
        });

        if($scope.agrupar == true) {
          $scope.porcentajesPrestamo();
        }
      }
      
    }])


    //****************************************************
    //ESTADO DE CUENTA SOCIO                             *
    //****************************************************
    .controller('EstadoCuentaCtrl', ['$scope', '$filter', '$timeout', '$window', 'MaestraPrestamoService', 'appService', 'AhorroServices', 'SolicitudPrestamoService',
                                        function ($scope, $filter, $timeout, $window, MaestraPrestamoService, appService, AhorroServices, SolicitudPrestamoService) {
      
      //Inicializar variables
      $scope.mostrar = 'ocultar';
      $scope.mostrar2 = 'ocultar';
      $scope.mostrar3 = 'ocultar';

      $scope.cuotasQ1Prestamos = 0;
      $scope.cuotasQ2Prestamos = 0;
      $scope.cuotasQ1Ordenes = 0;
      $scope.cuotasQ2Ordenes = 0;

      $scope.totalQ1 = 0;
      $scope.totalQ2 = 0;

      $scope.keyGetData = function($event) {
        if($event.keyCode == 13) {
          $scope.getData($event);
        }
      }

      $scope.getData = function($event) {
        $event.preventDefault();
        $scope.mostrar = 'mostrar';

        try {

          //Limpiar Data
          $scope.prestamos = [];
          $scope.datos = {};
          $scope.ahorroTotal = '';
          $scope.prestamosTotal = '';
          $scope.totalQ1 = 0;
          $scope.totalQ2 = 0;
          $scope.DISPONIBLE = 0;
          //Fin Limpiar Data

          MaestraPrestamoService.EstadoCuentaBySocio($scope.codigoSocio).then(function (data) {
            $scope.mostrar = 'mostrar';
            $scope.mostrar2 = 'mostrar';

            console.log(data);
            $scope.datos = data[0];
            
            //Traer todos los prestamos activos.
            MaestraPrestamoService.PrestamosbySocio($scope.codigoSocio).then(function (data) {
              console.log('Prestamos del socio');
              console.log(data);


              $scope.prestamos = data;

              $scope.prestamos.forEach(function (item) {
                if(item.noSolicitudOD > 0) {
                  $scope.cuotasQ1Ordenes += item.montoCuotaQ1;
                  $scope.cuotasQ2Ordenes += item.montoCuotaQ2;
                } else {
                  $scope.cuotasQ1Prestamos += item.montoCuotaQ1;
                  $scope.cuotasQ2Prestamos += item.montoCuotaQ2;
                }
              });

              $scope.mostrar2 = 'ocultar';
              console.log($scope.ahorroTotal);
              console.log($scope.prestamosTotal);

            },
            function (error) {
              $scope.mostrar2 = 'ocultar';
            });

            $scope.mostrar3 = 'mostrar';
            //Traer el ahorro capitalizado del socio
            AhorroServices.getAhorroSocio($scope.codigoSocio).then(function (data) {
              if(data.length > 0) {
                $scope.ahorroTotal = $filter('number')(data[0]['balance'], 2);
              } else {
                $scope.ahorroTotal = 0;
              }              

              $scope.mostrar3 = 'ocultar';

              //CALCULAR EL DISPONIBLE
              var disp = setTimeout(function () {
                $scope.DISPONIBLE = $filter('number') (parseFloat($scope.ahorroTotal.replaceAll(',','')) - parseFloat($scope.prestamosTotal.replaceAll(',','')), 2);
                console.log($scope.DISPONIBLE);
              },5000);

            },
            function (error) {
              $scope.mostrar3 = 'ocultar';
            });

            $scope.mostrar = 'mostrar';
            //Traer el balance de deudas (prestamos) del socio
            MaestraPrestamoService.prestamosBalanceByCodigoSocio($scope.codigoSocio).then(function (data) {
              
              if(data.length > 0) {
                $scope.prestamosTotal = $filter('number')(data[0]['balance'], 2);
              } else {
                $scope.prestamosTotal = 0;
              }

            });

            $scope.mostrar = 'ocultar';

            SolicitudPrestamoService.solicitanteDatos($scope.codigoSocio).then(function (data) {
              $scope.dataSolicitante = data[0];
              console.log('dataSolicitante');
              console.log($scope.dataSolicitante); 

              $scope.totalQ1 = $scope.dataSolicitante.cuotaAhorroQ1 + $scope.cuotasQ1Prestamos + $scope.cuotasQ1Ordenes;
              $scope.totalQ2 = $scope.dataSolicitante.cuotaAhorroQ2 + $scope.cuotasQ2Prestamos + $scope.cuotasQ2Ordenes;
            });

          });

        } catch(e) {
          console.log(e);
        }
      }

      $scope.totales = function() {
        $scope.totalMontoOriginal = 0.00;
        $scope.totalBalance = 0.00;

        $scope.totalMontoAgrupado = 0.00;
        $scope.totalCantidadAgrupado = 0;

        $scope.registros.forEach(function (documento) {
          if($scope.agrupar != undefined) {
            $scope.totalMontoAgrupado += parseFloat(documento.totalMonto);
            $scope.totalCantidadAgrupado += parseFloat(documento.totalCantidad);

          } else {
            $scope.totalMontoOriginal += parseFloat(documento.montoInicial.replaceAll(',',''));
            $scope.totalBalance += parseFloat(documento.balance.replaceAll(',',''));
          }
        });

        if($scope.agrupar == true) {
          $scope.porcentajesPrestamo();
        }
      }
      
    }])

    //****************************************************
    //RESUMEN ESTADO DE SOCIOS                           *
    //****************************************************
    .controller('ResumenEstadoCuentaCtrl', ['$scope', '$filter', '$timeout', '$window', 'MaestraPrestamoService', 'appService', 'AhorroServices', 'SolicitudPrestamoService', 'FacturacionService',
                                        function ($scope, $filter, $timeout, $window, MaestraPrestamoService, appService, AhorroServices, SolicitudPrestamoService, FacturacionService) {
      
      //Inicializar variables
      $scope.mostrar = 'ocultar';
      $scope.allData = [];

      $scope.getData = function() {
        $scope.mostrar = 'mostrar';

        $scope.sociosFull = [];
        $scope.socioOne = {};

        try {

          //Traer todos los socios a javascript
          // FacturacionService.socios().then(function (data) {

          //   data.forEach(function (item) {
          //     $scope.socioOne = {};
          //     $scope.socioOne.codigo = item.codigo;
          //     $scope.socioOne.nombre = item.nombreCompleto;

          //     AhorroServices.getAhorroSocio(item.codigo).then(function (data) {
          //       if(data.length > 0) {
          //         $scope.ahorroTotal = $filter('number')(data[0]['balance'], 2);                  
          //       } else {
          //         $scope.ahorroTotal = 0;
          //       }

          //       $scope.socioOne.ahorros = $scope.ahorroTotal;

          //       //Traer el balance de deudas (prestamos) del socio
          //       MaestraPrestamoService.prestamosBalanceByCodigoSocio(item.codigo).then(function (data) {
                  
          //         if(data.length > 0) {
          //           $scope.prestamosTotal = $filter('number')(data[0]['balance'], 2);
          //         } else {
          //           $scope.prestamosTotal = 0;
          //         }

          //         $scope.socioOne.prestamos = $scope.prestamosTotal;
          //         $scope.sociosFull.push($scope.socioOne);

          //       });
          //     },
          //       function (error) {
          //         $scope.mostrar = 'ocultar';
          //     });

          //   console.log('TERMINO: ' + item.nombreCompleto);

          //   });

          //   $scope.mostrar = 'ocultar';
          // });

          AhorroServices.getAllAhorro().then(function (data) {
            console.log(data);
          }); 

        } catch(e) {
          console.log(e);
        }
      }

      $scope.cargar = function($event) {
        $event.preventDefault();

        $scope.allData = $scope.sociosFull;

      }

    }]);
      
})(_);