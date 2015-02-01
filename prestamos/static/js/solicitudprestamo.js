(function (_) {

  angular.module('cooperativa.solicitudprestamo', ['ngAnimate'])

    .filter('estatusSolicitud', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('A', true)
                .replace('R', true)
                .replace('C', true);
        return input;
      }
    })

    .filter('estatusName', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('A', 'Aprobado')
                .replace('P', 'En Proceso')
                .replace('R', 'Rechazado')
                .replace('C', 'Cancelado');
        return input;
      }
    })

    .factory('SolicitudPrestamoService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Solicitud de Prestamo
      function guardaSolicitudPrestamo(solicitante, solicitud, fechaSolicitud, fechaDescuento) {
        var deferred = $q.defer();

        $http.post('/prestamos/solicitudP/', JSON.stringify({'solicitante': solicitante, 
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

      // Aprobar/Rechazar solicitudes de prestamos.
      function AprobarRechazarSolicitudes(solicitudes, accion) {
        var deferred = $q.defer();

        $http.post('/prestamos/solicitudP/AprobarRechazar', JSON.stringify({'solicitudes': solicitudes, 'accion': accion})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Llenar el listado de Solicitudes
      function solicitudesprestamos(noSolicitud) {
        var deferred = $q.defer();
        var url = "/api/prestamos/solicitudes/prestamos/?format=json";

        if (noSolicitud != undefined) {
            url = "/api/prestamos/solicitudes/prestamos/noSolicitud/?format=json".replace('noSolicitud', noSolicitud);
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Filtrar el listado de Solicitudes por Socio
      function solicitudesprestamosBySocio(dato) {
        var deferred = $q.defer();
        var url = "";

        if(!isNaN(dato)) {
          url = "/api/prestamos/solicitudes/prestamos/codigo/dato/?format=json".replace("dato", dato);
        } else {
          url = "/api/prestamos/solicitudes/prestamos/nombre/dato/?format=json".replace("dato", dato);
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Filtrar el listado de Solicitudes por estatus
      function solicitudesprestamosByEstatus(estatus) {
        var deferred = $q.defer();

        solicitudesprestamos(undefined).then(function (data) {
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

      //Socio por Codigo de Empleado
      function SocioByCodigoEmpleado(codigo) {
        var deferred = $q.defer();

        if(codigo != undefined) {
          url = '/api/socio/idempleado/codigo/?format=json'.replace('codigo', codigo);
        } else {
          url = '/api/socio/idempleado/?format=json'
        }

        http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Categorias de prestamos.
      function categoriasPrestamos(id, categoria) {
        var deferred = $q.defer();

        console.log(categoria);
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
                return registros.tipo == 'PR';
              }));
            }
          });

        return deferred.promise;
      }

      //Cantidad de Cuotas de Prestamo (parametro: monto)
      function cantidadCuotasPrestamoByMonto(monto) {
        var deferred = $q.defer();
        var url = "/api/cantidadCuotasPrestamos/monto/?format=json".replace("monto", monto.toString().replace(',',''));

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Buscar una solicitud en especifico (Desglose)
      function SolicitudPById(NoSolicitud) {
        var deferred = $q.defer();
        var doc = NoSolicitud != undefined? NoSolicitud : 0;

        $http.get('/solicitudPjson/?nosolicitud={solicitud}&format=json'.replace('{solicitud}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Autorizadores
      function getAutorizadores() {
        var deferred = $q.defer();

        $http.get('/api/autorizador/')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }


      return {
        solicitudesprestamos          : solicitudesprestamos,
        solicitudesprestamosBySocio   : solicitudesprestamosBySocio,
        solicitudesprestamosByEstatus : solicitudesprestamosByEstatus,
        SocioByCodigoEmpleado         : SocioByCodigoEmpleado,
        categoriasPrestamos           : categoriasPrestamos,
        cantidadCuotasPrestamoByMonto : cantidadCuotasPrestamoByMonto,
        guardaSolicitudPrestamo       : guardaSolicitudPrestamo,
        AprobarRechazarSolicitudes    : AprobarRechazarSolicitudes,
        SolicitudPById                : SolicitudPById,
        getAutorizadores              : getAutorizadores 
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('SolicitudPrestamoCtrl', ['$scope', '$filter', 'SolicitudPrestamoService', 'FacturacionService',
                                        function ($scope, $filter, SolicitudPrestamoService, FacturacionService) {
      
      //Inicializacion de variables
      $scope.showCP = false; //Mostrar tabla que contiene las categorias de prestamos
      $scope.tableSocio = false; //Mostrar tabla que contiene los socios
      $scope.showLSP = true; //Mostrar el listado de solicitudes

      $scope.disabledButton = 'Boton-disabled';
      $scope.disabledButtonBool = true;

      $scope.regAll = false;
      $scope.estatus = 'T';

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

        SolicitudPrestamoService.solicitudesprestamos(noSolicitud).then(function (data) {
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

      $scope.solicitudesprestamosBySocio = function($event, socio) {

        if($event.keyCode == 13) {

          SolicitudPrestamoService.solicitudesprestamosBySocio(socio).then(function (data) {

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
          SolicitudPrestamoService.solicitudesprestamosByEstatus(estatus).then(function (data) {

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

      //Traer todas las categorias de prestamos (de tipo PRESTAMO)
      $scope.categoriasPrestamos = function(id, $event) {
        $event.preventDefault();
        var descrp = '';

        if($event.type != 'click') {
          descrp = $scope.solicitud.categoriaPrestamo;
        }

        try {

          SolicitudPrestamoService.categoriasPrestamos(id, descrp).then(function (data) {
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

      //Cantidad de cuotas (parametro: monto)
      $scope.getCantidadCuotasPrestamo = function(monto) {
        try {
          SolicitudPrestamoService.cantidadCuotasPrestamoByMonto(monto).then(function (data) {
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
        $scope.solicitud.tasaInteresAnual = cp.interesAnualSocio;
        $scope.solicitud.tasaInteresMensual = cp.interesAnualSocio / 12;
        $scope.showCP = false;
      }

      //Cuando se le de click al checkbox del header.
      $scope.seleccionAll = function() {

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

          $scope.solicitudesSeleccionadas.splice($scope.solicitudesSeleccionadas[index],1);
        }
      }

      //Nueva Entrada de Factura
      $scope.nuevaEntrada = function(usuario) {
        $scope.solicitante = {};
        $scope.solicitud = {};

        $scope.solicitante.representanteCodigo = 16; //CAMBIAR ESTO
        $scope.solicitante.representanteNombre = 'EMPRESA'; //CAMBIAR ESTO
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


      //Guardar Factura
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

          if(fechaDescuentoFormatted < $filter('date')(Date.now(), 'yyyy-MM-dd')) {
            $scope.mostrarError("La fecha para descuento no puede ser menor a la fecha de hoy.");
            throw "La fecha para descuento no puede ser menor a la fecha de hoy.";
          }
          if(fechaSolicitudFormatted < $filter('date')(Date.now(), 'yyyy-MM-dd')) {
            $scope.mostrarError("La fecha para solicitud no puede ser menor a la fecha de hoy.");
            throw "La fecha para solicitud no puede ser menor a la fecha de hoy.";
          }

          if($scope.solicitud.valorGarantizado == undefined) {
            $scope.solicitud.valorGarantizado = '0';
          }
          if($scope.solicitud.prestacionesLaborales == undefined) {
            $scope.solicitud.prestacionesLaborales = '0';
          }

          SolicitudPrestamoService.guardaSolicitudPrestamo($scope.solicitante,$scope.solicitud, fechaSolicitudFormatted, fechaDescuentoFormatted).then(function (data) {
            if(isNaN(parseInt(data))) {
              $scope.mostrarError(data);
              throw data;
            }
            $scope.solicitud.solicitudNo = $filter('numberFixedLen')(data, 8)

            $scope.disabledButton = 'Boton-disabled';
            $scope.disabledButtonBool = true;

            $scope.errorShow = false;
            $scope.listadoSolicitudes();
            $scope.toggleLSP();
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

      // Autoriazadores
      $scope.autorizadores = function() {
        SolicitudPrestamoService.getAutorizadores().then(function (data) {
          if(data.length > 0) {
            $scope.autorizadores = data;
          }

        });
      }

      // Cancelar llenado de solicitud 
      $scope.cancelarSolicitud = function($event) {
        $event.preventDefault();

        $scope.nuevaEntrada();
        $scope.toggleLSP();
      } 

      // Aprobar/Rechazar solicitudes de prestamos
      $scope.AprobarRechazarSolicitudesPrestamos = function($event, accion, solicitud) {
        $event.preventDefault();

        try {
          if(accion == 'C') {
            $scope.solicitudesSeleccionadas = [];
            $scope.solicitudesSeleccionadas.push(solicitud);
          }

          SolicitudPrestamoService.AprobarRechazarSolicitudes($scope.solicitudesSeleccionadas, accion).then(function (data) {
            if(data == 1) {
              $scope.listadoSolicitudes();
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
          SolicitudPrestamoService.SolicitudPById(solicitud).then(function (data) {

            if(data.length > 0) {
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

    }]);

})(_);