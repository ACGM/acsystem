var gulp = require('gulp'),
	connect =require('gulp-connect'),
	jshint= require('gulp-jshint'),
	stylish= require('jshint-stylish'),
	uglify= require('gulp-uglify'),
	gulpif= require('gulp-if'),
	minify= require('gulp-minify-css'),
	useref= require('gulp-useref'),
	concant= require('gulp-concat'),
	nib= require('nib'),
	stylus=require('stylus'),
	templateCache= require('gulp-angular-templatecache'),
	historyApiFallback = require('connect-history-api-fallback');

//Servidor web para gulp
gulp.task('server',function(){
	connect.server({
		root: './cxp',
		host: '0.0.0.0',
		port: 8080,
		livereload: true,
		middleweare:function(connect, opt){
			return [historyApiFallback];
		}
		});

	});

//tarea para manejar la cache de los template de angular
gulp.task('templatesAhorro',function(){
	gulp.src('./cxp/templates/*.html')
	.pipe(templateCache({
		root:'templates',
		module: 'cooperativa.cxp',
		standalone:true
	}))
	.pipe(gulp.dest('./cxp/static/js'));
});
//tarea uglifucadora para JS
gulp.task('jsCxp',function(){
	gulp.src('./cxp/static/js/libs')
		.pipe(gulpif('*.js',uglify({mangle:false})))
		.pipe(gulp.dest('./cxp/static/js'));
});

//tarea de Stylus para css
gulp.task('css', function(){
	gulp.src('./acgm/static/stylus/estilos.styl')
		.pipe(stylus({ use:nib() }))
		.pipe(gulp.dest('./acgm/static/css'))
		.pipe(connect.reload());
	});

//Recarga el servidor web cuando haya cambios en el HTML.
gulp.task('htmlCxp',function(){
	gulp.src('./cxp/templates/*.html')
		.pipe(connect.reload());
	});

//busca errores en el JavaScript y "Los muestra en pantalla ", ay que probarlo jajajaja
gulp.task('jshintCxp',function(){
	return gulp.src('./cxp/static/js/libs/*.js')
			.pipe(jshint())
			.pipe(jshint.reporter('jshint-stylish'))
			.pipe(jshint.reporter('fail'));
	});

//Lanza las tareas cuando detecta cambios
gulp.task('watch', function(){

	gulp.watch(['./cxp/static/js/libs/*.js'],['jsCxp']);

	//proceso de watch para css
	//gulp.watch(['./acgm/static/stylus/*.styl'],['css']);

	//Proceso de watch para ahorro
	gulp.watch(['./cxp/templates/*.html'],['htmlCxp']);

	//Proceso de watch para jshint
	gulp.watch(['./cxp/static/js/libs/*.js','./Gulpfile.js'],['jshintCxp']);

	});

//lanza la tarea por defaul, correr el servidor y las tareas de watch
gulp.task('default',['server','watch']);
