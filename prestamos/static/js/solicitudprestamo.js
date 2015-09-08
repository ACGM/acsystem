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
      function guardaSolicitudPrestamo(solicitante, solicitud, fechaSolicitud, fechaDescuento, prestamosUnificados) {
        var deferred = $q.defer();

        $http.post('/prestamos/solicitudP/', JSON.stringify({'solicitante': solicitante, 
                                                              'solicitud': solicitud, 
                                                              'fechaSolicitud': fechaSolicitud,
                                                              'fechaDescuento': fechaDescuento,
                                                              'prestamosUnificados': prestamosUnificados})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      // Validar Autorizador
      function ValidaAutorizador(autorizador, pin) {
        var deferred = $q.defer();

        $http.post('/prestamos/validaAutorizador/', JSON.stringify({'autorizador': autorizador, 'pin': pin})).
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

        $http.post('/prestamos/solicitudP/AprobarRechazar/', JSON.stringify({'solicitudes': solicitudes, 'accion': accion})).
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

      //Representantes
      function getRepresentantes() {
        var deferred = $q.defer();

        $http.get('/api/representante/')
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Solicitudes de Prestamos Emitadas en un rango de fecha.
      function solicitudesPrestamosEmitidas(fechaI, fechaF) {
        var deferred = $q.defer();

        var fechaInicio = fechaI.split('/');
        var fechaInicioFormatted = fechaInicio[2] + '-' + fechaInicio[1] + '-' + fechaInicio[0];

        var fechaFin = fechaF.split('/');
        var fechaFinFormatted = fechaFin[2] + '-' + fechaFin[1] + '-' + fechaFin[0];

        var url = "/api/prestamos/solicitudes/prestamos/emitidos/{fechaI}/{fechaF}/?format=json".replace("{fechaI}", fechaInicioFormatted).replace('{fechaF}', fechaFinFormatted);

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Datos completivos para solicitante
      function solicitanteDatos(codigo) {
        var deferred = $q.defer();

        url = "/api/socio/{codigo}/?format=json".replace('{codigo}', codigo);

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Interes de Prestamo Base Ahorro  -- Este es el beneficio de poner un % de interes menor por el ahorro capitalizado del socio.
      function getInteresPrestBaseAhorro() {
        var deferred = $q.defer();

        $http.get('/api/interesPrestamosBaseAhorro/?format=json')
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
        getAutorizadores              : getAutorizadores,
        getRepresentantes             : getRepresentantes,
        ValidaAutorizador             : ValidaAutorizador,
        solicitudesPrestamosEmitidas  : solicitudesPrestamosEmitidas,
        solicitanteDatos              : solicitanteDatos,
        getInteresPrestBaseAhorro     : getInteresPrestBaseAhorro
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('SolicitudPrestamoCtrl', ['$scope', '$filter', '$window', 'SolicitudPrestamoService', 'FacturacionService', 'MaestraPrestamoService',
                                        function ($scope, $filter, $window, SolicitudPrestamoService, FacturacionService, MaestraPrestamoService) {
      
      //Inicializacion de variables
      $scope.mostrar = 'mostrar';
      $scope.showCP = false; //Mostrar tabla que contiene las categorias de prestamos
      $scope.tableSocio = false; //Mostrar tabla que contiene los socios
      $scope.showLSP = true; //Mostrar el listado de solicitudes

      $scope.disabledButton = 'Boton-disabled';
      $scope.disabledButtonBool = true;

      $scope.regAll = false;
      $scope.estatus = 'T';

      $scope.item = {};
      $scope.solicitudes = {};

      $scope.prestamosSocioUnif = [];
      $scope.solicitudesSeleccionadas = [];
      $scope.reg = [];
      $scope.valoresChk = [];

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLD = 'UpArrow';

      //Traer todos los socios a javascript
      FacturacionService.socios().then(function (data) {
        $scope.todosLosSocios = data;
      });

      SolicitudPrestamoService.getInteresPrestBaseAhorro().then(function (data) {
        $scope.InteresPrestBaseAhorroAnual = data[0]['porcentajeAnual'];
      })

      window.onresize = function(event) {
        panelesSize();
      }

      function panelesSize() {
        document.getElementById('panelPrestamos').style.height = (window.innerHeight - 280) + 'px';
      }
      
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
        $scope.mostrar = 'mostrar';
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
            $scope.mostrar = 'ocultar';
          }
        }, function() {
          $scope.mostrar = 'ocultar';
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
          
          $scope.socios = $scope.todosLosSocios.filter(function (registro) {
            return registro.codigo.toString().substring(0, $scope.solicitante.codigoEmpleado.length) == $scope.solicitante.codigoEmpleado;
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

       //Seleccionar Socio
      $scope.selSocio = function($event, s) {
        $event.preventDefault();

        $scope.solicitante.codigoEmpleado = s.codigo;
        $scope.solicitante.nombreEmpleado = s.nombreCompleto;
        $scope.solicitante.cedula = s.cedula;
        $scope.solicitante.salario = $filter('number')(s.salario,2);
        $scope.tableSocio = false;

        $scope.getPrestamosBalances(s.codigo); //Buscar prestamos para unificar.

        MaestraPrestamoService.prestamosBalanceByCodigoSocio(s.codigo).then(function (data) {

          if(data.length > 0) {
            $scope.solicitud.deudasPrestamos = $filter('number')(data[0]['balance'], 2);
          } else {
            $scope.solicitud.deudasPrestamos = 0;
          }
        });
      }

      //Seleccionar Categoria de Prestamo
      $scope.selCP = function($event, cp) {
        $event.preventDefault();

        $scope.solicitud.categoriaPrestamoId = cp.id;
        $scope.solicitud.categoriaPrestamo = cp.descripcion;
        $scope.solicitud.tasaInteresAnual = $filter('number')(cp.interesAnualSocio, 2);
        $scope.solicitud.tasaInteresMensual = $filter('number')((cp.interesAnualSocio / 12), 2);
        $scope.showCP = false;

        //Calcular los intereses y la cuota capital+intereses.
        var valorGarant = $scope.solicitud.valorGarantizado == undefined? $scope.solicitud.prestacionesLaborales : $scope.solicitud.valorGarantizado;
        calculosCuotaIntereses(valorGarant, $scope.solicitud.ahorrosCapitalizados.replace(',',''), $scope.solicitud.tasaInteresMensual, 
                                $scope.solicitud.valorCuotas);

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

      //Cuando se le de click a un checkbox de la lista de prestamos a unificar.
      $scope.selectedRegPU = function(iReg) {
        
        index = $scope.prestamosSocio.indexOf(iReg);

        if ($scope.reg[$scope.prestamosSocio[index].noPrestamo] === true){
          $scope.prestamosSocioUnif.push($scope.prestamosSocio[index]);
        }
        else{
          $scope.prestamosSocioUnif = _.without($scope.prestamosSocioUnif, _.findWhere($scope.prestamosSocioUnif, {noPrestamo : iReg.noPrestamo}));
        }

        console.log($scope.prestamosSocioUnif)
      }


      //Nueva Entrada de Factura
      $scope.nuevaEntrada = function(usuario) {
        $scope.solicitante = {};
        $scope.solicitud = {};
        $scope.prestamosSocioUnif = [];

        // $scope.solicitante.representanteCodigo = '';
        // $scope.solicitante.representanteNombre = undefined;
        $scope.solicitante.auxiliar = '';
        $scope.solicitante.cobrador = usuario;
        $scope.solicitante.autorizadoPor = usuario;

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

          SolicitudPrestamoService.guardaSolicitudPrestamo($scope.solicitante, 
                                                            $scope.solicitud, 
                                                            fechaSolicitudFormatted, 
                                                            fechaDescuentoFormatted,
                                                            $scope.prestamosSocioUnif).then(function (data) {
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
          console.log(e);
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

              $scope.solicitud.garante = data[0]['garante'];

              //Calcular los intereses y la cuota capital+intereses.
              var valorGarant = data[0]['valorGarantizado'] == '0'? data[0]['prestacionesLaborales'] : data[0]['valorGarantizado'];
              calculosCuotaIntereses(valorGarant, data[0]['ahorrosCapitalizados'], data[0]['tasaInteresMensual'], data[0]['valorCuotasCapital']);

              if(data[0]['estatus'] == 'P') {
                $scope.disabledButton = 'Boton';
                $scope.disabledButtonBool = false;
              } else {
                $scope.disabledButton = 'Boton-disabled';
                $scope.disabledButtonBool = true;
              }

              $scope.prestamosSocio = data[0]['PrestamosUnificados'];
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

      function calculosCuotaIntereses(valorGarantizado, ahorroCap, InteresMensual, CuotasCapital) {
        var interesBaseAhorroMensual = parseFloat($scope.InteresPrestBaseAhorroAnual/12/2/100);
        var IBA = (ahorroCap * interesBaseAhorroMensual);
        var IBG = valorGarantizado != undefined? valorGarantizado * (InteresMensual/2/100) : 0;
console.log(IBG)
        $scope.solicitud.tasaInteresBaseAhorro = $scope.InteresPrestBaseAhorroAnual/12;
        $scope.solicitud.interesBaseAhorro = $filter('number')(IBA, 2);
        $scope.solicitud.interesBaseGarantizado = $filter('number')(IBG, 2);
        $scope.solicitud.cuotaCapitalIntereses = $filter('number') (parseFloat(CuotasCapital.replace(',','')) + IBA + IBG, 2);
      }

      //Reporte Solicitudes de Prestamos Emitidas
      $scope.solprestamosEmitidas = function() {
        $scope.totalMontoSolicitado = 0;
        $scope.totalNetoDesembolsar = 0;

        try {
          SolicitudPrestamoService.solicitudesPrestamosEmitidas($scope.fechaInicio, $scope.fechaFin).then(function (data) {
            $scope.registros = data;
            console.log(data);

            if(data.length > 0) {
              data.forEach(function (item) {
                $scope.totalMontoSolicitado += parseFloat(item.montoSolicitado);
                $scope.totalNetoDesembolsar += parseFloat(item.netoDesembolsar);
              });
            }

          });
        } catch (e) {
          $scope.mostrarError(e);
          console.log(e);
        }
      }

      //Traer prestamos para unificar.
      $scope.getPrestamosBalances = function(socio) {
        try {
          MaestraPrestamoService.prestamosDetalleByCodigoSocio(socio).then(function (data) {

            if(data.length > 0) {
              $scope.prestamosSocioUnif = [];
              $scope.prestamosSocio = data.filter(function (item) {
                return item.balance > 0;
              });
            } else {
              throw data;
            }
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Imprimir solicitud de prestamo
      $scope.ImprimirSolicitud = function(solicitud) {
        $window.sessionStorage['solicitudP'] = JSON.stringify(solicitud);
        $window.open('/prestamos/print/solicitudP/', target='_blank'); 
      }

    }])

    //****************************************************
    //CONTROLLERS Imprimir Solicitud Prestamo            *
    //****************************************************
    .controller('ImprimirSolicitudPCtrl', ['$scope', '$filter', '$window', 'SolicitudPrestamoService', 'MaestraPrestamoService',
                                        function ($scope, $filter, $window, SolicitudPrestamoService, MaestraPrestamoService) {
      
      //Objeto que contiene la informacion de la solicitud de Prestamo
      $scope.solicitudP = JSON.parse($window.sessionStorage['solicitudP']);
      console.log($scope.solicitudP);

      //Calculo de intereses para sumar al capital
      var intG = ($scope.solicitudP.tasaInteresMensual / 2 / 100) * ($scope.solicitudP.prestacionesLaborales);
      var intA = ($scope.solicitudP.interesBaseAhorroMensual / 2 / 100) * ($scope.solicitudP.ahorrosCapitalizados);
      var intereses = intG + intA;

      $scope.solicitudP.capitalMasIntereses = intereses + parseFloat($scope.solicitudP.valorCuotasCapital);
      $scope.solicitudP.interesesValor = intereses;
      console.log($scope.solicitudP.capitalMasIntereses)

      //Objeto que contiene la informacion del solicitante
      SolicitudPrestamoService.solicitanteDatos($scope.solicitudP.codigoSocio).then(function (data) {
        $scope.dataSolicitante = data[0];
        console.log($scope.dataSolicitante);        

        //Calculo para cuota quincenal de prestamo
        var cuotaPrestamo;
        cuotaPrestamo = $scope.solicitudP.montoSolicitado * ($scope.solicitudP.tasaInteresMensual/100);
        cuotaPrestamo = $scope.solicitudP.valorCuotasCapital + cuotaPrestamo;
        $scope.varCuotaPrestamo = $scope.solicitudP.capitalMasIntereses;

        //Totales en Quincenas (ahorro y cuota Prestamo)
        $scope.totalQ1 = parseFloat($scope.dataSolicitante.cuotaAhorroQ1) + parseFloat($scope.varCuotaPrestamo);
        $scope.totalQ2 = parseFloat($scope.dataSolicitante.cuotaAhorroQ2) + parseFloat($scope.varCuotaPrestamo);

        //Porcentajes Endeudamiento
        $scope.porcentajeEndeuda1 = ($scope.totalQ1 / $scope.dataSolicitante.salario) * 100;
        $scope.porcentajeEndeuda2 = ($scope.totalQ2 / $scope.dataSolicitante.salario) * 100;

        //Monto al que aplica
        var prestLab = $scope.solicitudP.prestacionesLaborales != undefined? $scope.solicitudP.prestacionesLaborales : 0;
        var valorGaran = $scope.solicitudP.valorGarantizado != undefined? $scope.solicitudP.valorGarantizado : 0;
        var deudasPrest = $scope.solicitudP.deudasPrestamos != undefined? $scope.solicitudP.deudasPrestamos : 0;

        $scope.montoAplica = ($scope.solicitudP.ahorrosCapitalizados + 
                              parseFloat(prestLab) +
                              parseFloat(valorGaran)) - deudasPrest;
      });


      // SolicitudPrestamoService.SolicitudPById($scope.solicitudP.solicitudNo).then(function (data) {

      //   if(data.length > 0) {
      //     $scope.dataH.factura = $filter('numberFixedLen')($scope.factura.noFactura, 8);
      //     $scope.dataH.fecha = $filter('date')(data[0]['fecha'], 'dd/MM/yyyy');
      //     $scope.socioCodigo = data[0]['socioCodigo'];
      //     $scope.socioNombre = data[0]['socioNombre'];
      //     $scope.dataH.orden = $filter('numberFixedLen')(data[0]['orden'], 8);
      //     $scope.dataH.terminos = data[0]['terminos'].replace('CR', 'CREDITO').replace('CO', 'DE CONTADO');
      //     $scope.dataH.vendedor = data[0]['vendedor'];
      //     $scope.dataH.impresa = data[0]['impresa'];

      //     data[0]['productos'].forEach(function (item) {
      //       item.subtotal = parseFloat(item.descuento) > 0? (item.precio * item.cantidad) - ((item.descuento / 100) * item.cantidad * item.precio) : (item.precio * item.cantidad);
      //       $scope.dataD.push(item);
      //     });

      //     $scope.totalDescuento_ = $scope.totalDescuento();
      //     $scope.totalValor_ = $scope.totalValor();
      //   }
      // });

      $scope.imprimirSol = function() {

        FacturacionService.impresionFact($scope.factura.noFactura).then(function (data) {
          console.log("DATA: " + data);

          document.getElementById('printBoton').style.display = "None";
          window.print();
          window.location.reload();
          document.getElementById('printBoton').style.display = "";
        });
      }
       
     }]);

})(_);