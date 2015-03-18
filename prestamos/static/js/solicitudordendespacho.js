(function (_) {

  angular.module('cooperativa.solicitudod', ['ngAnimate'])

    .factory('SolicitudOrdenDespachoService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Solicitud de Orden de Despacho
      function guardaSolicitudOD(solicitante, solicitud, fechaSolicitud, fechaDescuento) {
        var deferred = $q.defer();

        $http.post('/prestamos/solicitudOD/', JSON.stringify({'solicitante': solicitante, 
                                                              'solicitud': solicitud, 
                                                              'fechaSolicitud': fechaSolicitud,
                                                              'fechaDescuento': fechaDescuento})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

       //Guardar Detalle de Solicitud de Orden de Despacho
      function guardaSolicitudODDetalle(solicitudNo, articulos) {
        var deferred = $q.defer();

        $http.post('/prestamos/solicitudOD/detalle/', JSON.stringify({'articulos': articulos, 'solicitudNo': solicitudNo})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      // Aprobar/Rechazar solicitudes de Ordenes de Despacho.
      function AprobarRechazarSolicitudes(solicitudes, accion) {
        var deferred = $q.defer();

        $http.post('/prestamos/solicitudOD/AprobarRechazar/', JSON.stringify({'solicitudes': solicitudes, 'accion': accion})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Llenar el listado de Solicitudes
      function solicitudesOD(noSolicitud) {
        var deferred = $q.defer();
        var url = "/api/prestamos/solicitudes/od/?format=json";

        if (noSolicitud != undefined) {
            url = "/api/prestamos/solicitudes/od/noSolicitud/?format=json".replace('noSolicitud', noSolicitud);
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Filtrar el listado de Solicitudes por Socio
      function solicitudesODBySocio(dato) {
        var deferred = $q.defer();
        var url = "";

        if(!isNaN(dato)) {
          url = "/api/prestamos/solicitudes/od/codigo/dato/?format=json".replace("dato", dato);
        } else {
          url = "/api/prestamos/solicitudes/od/nombre/dato/?format=json".replace("dato", dato);
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Filtrar el listado de Solicitudes por estatus
      function solicitudesODByEstatus(estatus) {
        var deferred = $q.defer();

        solicitudesOD(undefined).then(function (data) {
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

      //Categorias de prestamos (para ORDENES DE DESPACHO).
      function categoriasPrestamos(id, categoria) {
        var deferred = $q.defer();

        if(categoria != undefined && categoria != '') {
          url = '/api/categoriasPrestamos/{categoria}/?format=json'.replace('{categoria}', categoria);
        } else {
          url = '/api/categoriasPrestamos/?format=json';
        }

        $http.get(url)
          .success(function (data) {
            if (id != undefined) {
              deferred.resolve(data.filter(function (item) {
                return item.id == id;
              }));
            } else {
              deferred.resolve(data.filter(function (registros) {
                return registros.tipo == 'OD'; //PARA TIPO ORDEN DESPACHO
              }));
            }
          });

        return deferred.promise;
      }

      //Cantidad de Cuotas de Ordenes de Despacho (parametro: monto)
      function cantidadCuotasODByMonto(monto) {
        var deferred = $q.defer();
        var url = "/api/cantidadCuotasPrestamos/monto/?format=json".replace("monto", monto.toString().replace(',',''));

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Buscar una solicitud en especifico (Desglose)
      function SolicitudODById(NoSolicitud) {
        var deferred = $q.defer();
        var doc = NoSolicitud != undefined? NoSolicitud : 0;

        $http.get('/solicitudODjson/?nosolicitud={solicitud}&format=json'.replace('{solicitud}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      return {
        solicitudesOD                 : solicitudesOD,
        solicitudesODBySocio   : solicitudesODBySocio,
        solicitudesODByEstatus : solicitudesODByEstatus,
        categoriasPrestamos           : categoriasPrestamos,
        cantidadCuotasODByMonto : cantidadCuotasODByMonto,
        guardaSolicitudOD             : guardaSolicitudOD,
        AprobarRechazarSolicitudes    : AprobarRechazarSolicitudes,
        SolicitudODById               : SolicitudODById,
        guardaSolicitudODDetalle      : guardaSolicitudODDetalle
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('SolicitudODCtrl', ['$scope', '$filter', '$window', 'SolicitudOrdenDespachoService','SolicitudPrestamoService', 'FacturacionService', 'InventarioService',
                                function ($scope, $filter, $window, SolicitudOrdenDespachoService, SolicitudPrestamoService, FacturacionService, InventarioService) {
      
      //Inicializacion de variables
      $scope.showCP = false; //Mostrar tabla que contiene las categorias de prestamos
      $scope.tableSocio = false; //Mostrar tabla que contiene los socios
      $scope.showLSP = true; //Mostrar el listado de solicitudes

      $scope.disabledButton = 'Boton-disabled';
      $scope.disabledButtonBool = true;

      $scope.regAll = false;
      $scope.estatus = 'T';

      $scope.totalGeneralArticulos = 0;
      $scope.dataD = [];
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

        if ($scope.solicitud != undefined) {
          $scope.solicitud.solicitudNo = '0';
        }

        if($scope.showLSP === true) {
          $scope.ArrowLSP = 'UpArrow';
        } else {
          $scope.ArrowLSP = 'DownArrow';
        }
      }

      // Mostrar/Ocultar error
      $scope.toggleError = function() {
        $scope.errorShow = !$scope.errorShow;
      }


      //Listado de todas las solicitudes de prestamos
      $scope.listadoSolicitudes = function(noSolicitud) {
        $scope.solicitudesSeleccionadas = [];
        $scope.valoresChk = [];
        $scope.estatus = 'T';

        SolicitudOrdenDespachoService.solicitudesOD(noSolicitud).then(function (data) {
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

      $scope.solicitudesODBySocio = function($event, socio) {

        if($event.keyCode == 13) {

          SolicitudOrdenDespachoService.solicitudesODBySocio(socio).then(function (data) {

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

        try {
          SolicitudOrdenDespachoService.solicitudesODByEstatus(estatus).then(function (data) {

            if(data.length > 0) {
              $scope.solicitudes = data;

              $scope.verTodos = '';
              $scope.NoFoundDoc = '';

            } else {
              throw "No existen solicitudes con el estatus : " + $filter('estatusName')(estatus);
            }
          },
            function() {
              $scope.NoFoundDoc = "No existen solicitudes con el estatus : " + $filter('estatusName')(estatus);
            }
          );
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Traer todas las categorias de Prestamos (de tipo ORDEN DESPACHO)
      $scope.categoriasPrestamos = function(id, $event) {
        $event.preventDefault();
        var descrp = '';

        if($event.type != 'click') {
          descrp = $scope.solicitud.categoriaPrestamo;
        }

        try {
          SolicitudOrdenDespachoService.categoriasPrestamos(id, descrp).then(function (data) {
            if(data.length > 0) {
              $scope.categoriasP = data;
              $scope.showCP = true;
            }
            else {
              $scope.showCP = false;
            }
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Traer suplidores
      $scope.getSuplidor = function($event) {
        $event.preventDefault();
        var suplidor = '';

        if($event.type != 'click') {
          suplidor = $scope.solicitud.suplidorNombre;
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

      //Seleccionar Suplidor
      $scope.selSuplidor = function($event, supl) {
        $event.preventDefault();

        $scope.solicitud.idSuplidor = supl.id;
        $scope.solicitud.suplidorNombre = supl.nombre;
        $scope.tableSuplidor = false;
      }

      //Cantidad de cuotas (parametro: monto)
      $scope.getCantidadCuotasPrestamo = function(monto) {
        try {
          SolicitudOrdenDespachoService.cantidadCuotasODByMonto(monto).then(function (data) {
            if(data.length > 0) {
              $scope.solicitud.cantidadCuotas = data[0].cantidadQuincenas;

              $scope.solicitud.valorCuotas = $filter('number')(monto.replace(',','') / data[0].cantidadQuincenas,2);
            }
          },
          function() {
            $scope.mostrarError("No existe un rango para el monto neto a desembolsar.");
            throw "No existe un rango para el monto neto a desembolsar."
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Monto Neto a Desembolsar
      $scope.montoNeto = function() {
        var montoSolicitado = $scope.solicitud.montoSolicitado != undefined && $scope.solicitud.montoSolicitado != ''? parseFloat($scope.solicitud.montoSolicitado.replace(',','')) : 0;
        var ahorros = $scope.solicitud.ahorrosCapitalizados != undefined && $scope.solicitud.ahorrosCapitalizados != ''? parseFloat($scope.solicitud.ahorrosCapitalizados.replace(',','')) : 0;
        var deudas = $scope.solicitud.deudasPrestamos != undefined && $scope.solicitud.deudasPrestamos != ''? parseFloat($scope.solicitud.deudasPrestamos.replace(',','')) : 0;
        var garantizado = $scope.solicitud.valorGarantizado != undefined && $scope.solicitud.valorGarantizado != ''? parseFloat($scope.solicitud.valorGarantizado.replace(',','')) : 0;
        var prestaciones = $scope.solicitud.prestacionesLaborales != undefined && $scope.solicitud.prestacionesLaborales != ''? parseFloat($scope.solicitud.prestacionesLaborales.replace(',','')) : 0;

        var disponible = ahorros + garantizado + prestaciones - deudas;
        $scope.solicitud.montoDisponible = $filter('number')(disponible,2);

        if(montoSolicitado > disponible) {
          $scope.solicitud.netoDesembolsar = '';
          $scope.mostrarError("El monto solicitado no puede ser mayor a lo que tiene disponible.");
          throw "no disponible";
        } else {
          $scope.solicitud.netoDesembolsar = $filter('number')(montoSolicitado, 2);
          $scope.getCantidadCuotasPrestamo($scope.solicitud.netoDesembolsar);

          $scope.errorShow = false;
        }

      }

      //Traer Socios
      $scope.getSocio = function($event) {
        $event.preventDefault();

        $scope.tableSocio = true;

        if($scope.solicitante.codigoEmpleado != undefined) {
          FacturacionService.socios().then(function (data) {
            $scope.socios = data.filter(function (registro) {
              return registro.codigo.toString().substring(0, $scope.solicitante.codigoEmpleado.length) == $scope.solicitante.codigoEmpleado;
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

       //Seleccionar Socio
      $scope.selSocio = function($event, s) {
        $event.preventDefault();

        $scope.solicitante.codigoEmpleado = s.codigo;
        $scope.solicitante.nombreEmpleado = s.nombreCompleto;
        $scope.solicitante.cedula = s.cedula;
        $scope.solicitante.salario = $filter('number')(s.salario,2);
        $scope.tableSocio = false;
      }

      //Seleccionar Socio
      $scope.selCP = function($event, cp) {
        $event.preventDefault();

        $scope.solicitud.categoriaPrestamoId = cp.id;
        $scope.solicitud.categoriaPrestamo = cp.descripcion;
        $scope.solicitud.tasaInteresAnual = $filter('number')(cp.interesAnualSocio, 2);
        $scope.solicitud.tasaInteresMensual = $filter('number')(cp.interesAnualSocio / 12, 2);
        $scope.showCP = false;
      }

      //Cuando se le de click al checkbox del header.
      $scope.seleccionAll = function() {
        $scope.solicitudesSeleccionadas = [];

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

          $scope.solicitudesSeleccionadas = _.without($scope.solicitudesSeleccionadas, _.findWhere($scope.solicitudesSeleccionadas, {id : iReg.id}));
        }
      }

      //Nueva Entrada de Factura
      $scope.nuevaEntrada = function(usuario) {
        $scope.solicitante = {};
        $scope.solicitud = {};
        $scope.dataD = [];

        $scope.solicitante.representanteCodigo = '';
        $scope.solicitante.representanteNombre = undefined;
        $scope.solicitante.auxiliar = '';
        $scope.solicitante.cobrador = usuario;
        $scope.solicitante.autorizadoPor = '';

        $scope.solicitud.solicitudNo = 0;
        $scope.solicitud.valorGarantizado = undefined;
        $scope.solicitud.prestacionesLaborales = undefined;
        $scope.solicitud.nota = '';
        $scope.solicitud.deudasPrestamos = '';
        $scope.solicitud.fechaAprobacion = '';
        $scope.solicitud.fechaRechazo = '';
        $scope.solicitud.prestamo = '';

        $scope.solicitud.fechaSolicitud = $filter('date')(Date.now(),'dd/MM/yyyy');
        $scope.solicitud.fechaDescuento = $filter('date')(Date.now(),'dd/MM/yyyy');
        $scope.solicitud.ahorrosCapitalizados = "200,000";
        $scope.solicitud.deudasPrestamos = "50,000";

        $scope.showLSP = false;
        $scope.ArrowLSP = 'DownArrow';

        $scope.disabledButton = 'Boton';
        $scope.disabledButtonBool = false;

      }

      // Funcion para mostrar error por pantalla
      $scope.mostrarError = function(error) {
        $scope.errorMsg = error;
        $scope.errorShow = true;
      }


      //Guardar Solicitud de Prestamo
      $scope.guardarSolicitud = function($event) {
        $event.preventDefault();

        try {
          if (!$scope.SolicitudForm.$valid) {
            throw "Verifique que todos los campos esten completados correctamente.";
          }

          var fechaS = $scope.solicitud.fechaSolicitud.split('/');
          var fechaSolicitudFormatted = fechaS[2] + '-' + fechaS[1] + '-' + fechaS[0];

          var fechaP = $scope.solicitud.fechaDescuento.split('/');
          var fechaDescuentoFormatted = fechaP[2] + '-' + fechaP[1] + '-' + fechaP[0];

          //Exeptions
          if($scope.solicitante.validado != 'Correcto!') {
            // $scope.mostrarError("Verifique que haya digitado un pin de autorizador valido");
            throw "Verifique que haya digitado un pin de autorizador valido."
          }
          if(fechaDescuentoFormatted < $filter('date')(Date.now(), 'yyyy-MM-dd')) {
            $scope.mostrarError("La fecha para descuento no puede ser menor a la fecha de hoy.");
            throw "La fecha para descuento no puede ser menor a la fecha de hoy.";
          }
          if(fechaSolicitudFormatted < $filter('date')(Date.now(), 'yyyy-MM-dd')) {
            $scope.mostrarError("La fecha para solicitud no puede ser menor a la fecha de hoy.");
            throw "La fecha para solicitud no puede ser menor a la fecha de hoy.";
          }
          //End Exeptions

          if($scope.solicitud.valorGarantizado == undefined) {
            $scope.solicitud.valorGarantizado = '0';
          }
          if($scope.solicitud.prestacionesLaborales == undefined) {
            $scope.solicitud.prestacionesLaborales = '0';
          }

          SolicitudOrdenDespachoService.guardaSolicitudOD($scope.solicitante, $scope.solicitud, fechaSolicitudFormatted, fechaDescuentoFormatted).then(function (data) {
            if(isNaN(parseInt(data))) {
              $scope.mostrarError(data);
              throw data;
            }
            $scope.solicitud.solicitudNo = $filter('numberFixedLen')(data, 8)
            $scope.solicitud.estatus = 'P';

            $scope.disabledButton = 'Boton-disabled';
            $scope.disabledButtonBool = true;

            $scope.errorShow = false;
            $scope.listadoSolicitudes();
          },
          (function () {
            $scope.mostrarError('Hubo un error. Contacte al administrador del sistema.');
            throw 'Hubo un error. Contacte al administrador del sistema.';
          }
          ));

        }
        catch (e) {
          $scope.mostrarError(e);
        }
      }

      // Autoriazadores
      $scope.autorizadores = function() {
        SolicitudPrestamoService.getAutorizadores().then(function (data) {
          if(data.length > 0) {
            $scope.autorizadores = data;
          }
        });
      }

      // Representantes
      $scope.getRepresentantes = function() {
        SolicitudPrestamoService.getRepresentantes().then(function (data) {
          if(data.length > 0) {
            $scope.representantes = data;
          }
        });
      }

      // Cancelar llenado de solicitud 
      $scope.cancelarSolicitud = function($event) {
        $event.preventDefault();

        $scope.nuevaEntrada();
        $scope.toggleLSP();
      }

      // Seleccionar Autorizador
      $scope.selectAutorizador = function() {
        $scope.solicitante.autorizadorPin = '';
        $scope.solicitante.validado = '';
        $scope.solicitante.pinValido = false;
      }

      // Valida autorizador mediante ENTER
      $scope.validaAutorizadorKey = function($event) {
        
        if($event.keyCode == 13) {
          $scope.validarAutorizador($event);
        }
      }

      // Validar autorizador
      $scope.validarAutorizador = function($event) {
        $event.preventDefault();

        try {
          SolicitudPrestamoService.ValidaAutorizador($scope.solicitante.autorizadoPor, $scope.solicitante.autorizadorPin).then(function (data) {
            if(isNaN(parseInt(data))) {
              $scope.solicitante.validado = '';
              $scope.mostrarError('El pin que ha digitado es incorrecto.');
              $scope.solicitante.pinValido = false;
              $scope.solicitante.validado = 'Incorrecto!';
              throw data;
            } else {
              $scope.solicitante.validado = 'Correcto!';
              $scope.solicitante.pinValido = true;
              $scope.errorShow = false;
            }

          })
        } catch(e) {
          $scope.mostrarError(e);
        }
      }

      // Aprobar/Rechazar solicitudes de Orden de Despacho
      $scope.AprobarRechazarSolicitudesOD = function($event, accion, solicitud) {
        $event.preventDefault();

        try {
          if(accion == 'C') {
            $scope.solicitudesSeleccionadas = [];
            $scope.solicitudesSeleccionadas.push(solicitud);
          }

          SolicitudOrdenDespachoService.AprobarRechazarSolicitudes($scope.solicitudesSeleccionadas, accion).then(function (data) {
            if(data == 1) {
              $scope.listadoSolicitudes();
            } else {
              $scope.mostrarError(data);
              throw data;
            }
          },
          function() {
            $scope.mostrarError(data);
            throw data;
          });

        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      // Visualizar Solicitud de Prestamo (desglose)
      $scope.SolicitudFullById = function($event, solicitud) {
        $event.preventDefault();

        try {
          SolicitudOrdenDespachoService.SolicitudODById(solicitud).then(function (data) {

            if(data.length > 0) {
              $scope.dataD = [];
              $scope.errorMsg = '';
              $scope.errorShow = false;

              //completar los campos
              $scope.nuevaEntrada();

              $scope.solicitante.codigoEmpleado = data[0]['socioCodigo'];
              $scope.solicitante.nombreEmpleado = data[0]['socioNombre'];
              $scope.solicitante.representanteCodigo = data[0]['representanteCodigo'];
              $scope.solicitante.representanteNombre = data[0]['representanteNombre'];
              $scope.solicitante.auxiliar = ''; //data[0]['auxiliar'];
              $scope.solicitante.cedula = data[0]['socioCedula'];
              $scope.solicitante.salario = $filter('number')(data[0]['socioSalario'],2);
              $scope.solicitante.cobrador = data[0]['cobrador'];

              $scope.solicitante.autorizadoPor = data[0]['autorizadoPor'];
              $scope.solicitante.autorizadorPin = '****';
              $scope.solicitante.validado = 'Correcto!';
              $scope.solicitante.pinValido = true;
              $scope.solicitante.autorizadorFill = true;

              $scope.solicitud.montoSolicitado = data[0]['montoSolicitado']; //$filter('number')(data[0]['montoSolicitado'],2);
              $scope.solicitud.fechaSolicitud = $filter('date')(data[0]['fechaSolicitud'], 'dd/MM/yyyy');
              $scope.solicitud.ahorrosCapitalizados = $filter('number')(data[0]['ahorrosCapitalizados']);
              $scope.solicitud.deudasPrestamos = $filter('number')(data[0]['deudasPrestamos'],2);
              $scope.solicitud.prestacionesLaborales = data[0]['prestacionesLaborales']; //$filter('number')(data[0]['prestacionesLaborales'],2);
              $scope.solicitud.valorGarantizado = $filter('number')(data[0]['valorGarantizado'],2);
              $scope.solicitud.netoDesembolsar = $filter('number')(data[0]['netoDesembolsar']);
              $scope.solicitud.nota = data[0]['observacion'];
              $scope.solicitud.categoriaPrestamoId = data[0]['categoriaPrestamoId'];
              $scope.solicitud.categoriaPrestamo = data[0]['categoriaPrestamoDescrp'];
              $scope.solicitud.idSuplidor = data[0]['idSuplidor'];
              $scope.solicitud.suplidorNombre = data[0]['suplidorNombre'];
              $scope.solicitud.fechaDescuento = $filter('date')(data[0]['fechaParaDescuento'],'dd/MM/yyyy');
              $scope.solicitud.tasaInteresAnual = data[0]['tasaInteresAnual'];
              $scope.solicitud.tasaInteresMensual = data[0]['tasaInteresMensual'];
              $scope.solicitud.cantidadCuotas = data[0]['cantidadCuotas'];
              $scope.solicitud.valorCuotas = $filter('number')(data[0]['valorCuotasCapital'],2);
              $scope.solicitud.fechaAprobacion = data[0]['fechaAprobacion'] != undefined? $filter('date')(data[0]['fechaAprobacion'],'dd/MM/yyyy') : '';
              $scope.solicitud.fechaRechazo = data[0]['fechaRechazo'] != undefined? $filter('date')(data[0]['fechaRechazo'],'dd/MM/yyyy') : '';
              $scope.solicitud.solicitudNo = $filter('numberFixedLen')(data[0]['noSolicitud'],8);
              $scope.solicitud.prestamo = data[0]['prestamo'] != undefined? $filter('numberFixedLen')(data[0]['prestamo'],8) : '';
              $scope.solicitud.estatus = data[0]['estatus'];

              data[0]['articulos'].forEach(function (item) {
                $scope.dataD.push(item);
              });

              $scope.calculaTotales();

              if(data[0]['estatus'] == 'P') {
                $scope.disabledButton = 'Boton';
                $scope.disabledButtonBool = false;
              } else {
                $scope.disabledButton = 'Boton-disabled';
                $scope.disabledButtonBool = true;
              }

              $scope.solicitud.prestamosUnificados = data[0]['PrestamosUnificados'];
            }

          }, 
            (function () {
              $scope.mostrarError('No pudo encontrar el desglose de la solicitud #' + solicitud);
            }
          ));
        }
        catch (e) {
          $scope.mostrarError(e);
        }

        $scope.toggleLSP();
      }

      //Agregar Articulo de Orden Despacho
      $scope.agregarArticulo = function($event) {
        $event.preventDefault();

        var item = {};
        item.articulo = $scope.articulo.toUpperCase();

        if($event.type == 'keyup' && $event.keyCode == 13 || $event.type == 'click') {
          if(item.articulo.length > 0) {
            item.descuento = 0;
            $scope.dataD.push(item);
            $scope.articulo = '';
          }
        }
      }

      //Eliminar articulo de la lista de entradas
      $scope.eliminarArticulo = function($event, item) {
        $event.preventDefault();
        
        try {
          $scope.dataD = _.without($scope.dataD, _.findWhere($scope.dataD, {articulo: item.articulo}));

          $scope.calculaTotales();
          
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Calcula total de articulos ingresados
      $scope.calculaTotales = function () {
        $scope.totalGeneralArticulos = 0;
        var descuento = 0;

        $scope.dataD.forEach(function (item) {
          valor = item.cantidad * item.precio;

          if(!isNaN(valor)) {
            if (item.descuento != undefined && item.descuento > 0) {
              descuento = parseFloat(item.descuento/100);
              descuento = (item.precio * descuento * item.cantidad);
            } else {descuento=0}

            $scope.totalGeneralArticulos += valor - descuento;
          }
        });
      }

      //Guardar detalle de solicitud (articulos)
      $scope.guardarDetalleSolicitud = function() {
        if($scope.ArticulosODForm) {
          SolicitudOrdenDespachoService.guardaSolicitudODDetalle($scope.solicitud.solicitudNo, $scope.dataD).then(function (data) {
            if(data == 1) {
              alert('Se guardó perfectamente!');
            } else {
              $scope.mostrarError(data);
            }
          });
        }
      }

      //Imprimir Orden de Despacho
      $scope.ImprimirOD = function(solicitud) {
        $window.sessionStorage['noSolicitud'] = JSON.stringify(solicitud);
        $window.open('/solicitudOD/print/{noSolicitud}'.replace('{noSolicitud}',solicitud.noSolicitud), target='_blank'); 
      }

    }]);

})(_);