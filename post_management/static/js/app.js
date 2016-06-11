var app = angular.module('clientApp', ['ngRoute',])

app.config(['$routeProvider', function($routeProvider){
	$routeProvider
		.when('/', {
			controller: 'indexController',
			templateUrl: '/feedpost_management/static/partial/blog_feed.html'
		})
		.when('/topic/:id', {
			controller: 'postController',
			templateUrl: '/feedpost_management/static/partial/post.html'
		})
}])

app.service('social', ['$window', '$q', '$http', function($window, $q, $http) {
	var promise = null;
	var data = null;
	var retries = 0
	$window.resolve = function(_data) {
		data = _data;
		promise.resolve();
	}

	function comment(text, id) {
		$http({
			method:'POST',
			url: '/social/comment/'+id,
			data: {'comment_text': text}
		}).success(function(data, status) {
			console.log(data)
			retries = 0;
		}).error(function(data, status) {
			if(status == 401 && retries<3)
				openWindow(function(data) {
					retries+=1;
					comment(text, id)
				})
		})
	}

	function saveComment(id, data, callback) {
		$http({
			method:'PUT', 
			url: '/social/comment/'+id,
			data: data
		}).success(function(_data,status) {
			callback(data);
		})
	}

	function deleteComment(id) {
		$http({
			method: 'DELETE',
			url: '/social/comment/'+id,
		}).success(function() {
			console.log('deleted');
		})
	}

	function like (id) {
		$http({
			method:'POST',
			url: '/social/like/'+id,
		}).success(function(data, status) {
			console.log(data)
			retries = 0;
		}).error(function(data, status) {
			if(status == 401 && retries<3)
				openWindow(function(data) {
					retries+=1;
					comment(text, id)
				})
		})
	}

	var openWindow = function(callback) {
		promise = $q.defer();
		var v = $window.open('https://www.facebook.com/dialog/oauth?client_id=1653101508290097&redirect_uri=http://localhost:5000/social/auth/fb','','scrollbars=1')
		
		$q.when(promise).then(function() {
			callback(data)
		})
	}
	return {
		like : like,
		comment : comment,
		deleteComment: deleteComment,
		saveComment: saveComment,
		openWindow : openWindow
	}
}])

app.controller('indexController', ['$http', '$scope','$location',  function($http, $scope, $location) {
	$scope.getPosts = function() {
		$http({
			url: '/feed/api/post',
			method: 'GET'
		}).success(function(data) {

			$scope.posts = data.data;
		})
	}
	$scope.redirect = function(id) {
		$(document).scrollTop(0)
		$location.url('topic/'+id)
	}
	$scope.getPosts();
}])

app.controller('postController', ['$http', '$scope', '$routeParams','social', function($http,$scope, $routeParams, social) {
	var md = new showdown.Converter({tables:true})
	md.setOption('tables', true);
	
	$scope.getPost = function() {
		var id = $routeParams.id;

		$http({
			url: '/feed/api/post/'+id,
			method: 'GET'
		}).success(function(data) {
			$('.article-text').append(md.makeHtml(data.data.text))
			$scope.id = id
			$scope.post = data.data;
			$scope.post.create_date = new Date($scope.post.create_date);
		})
	}
	$scope.comment = function() {
		social.comment($scope.comment_text, $scope.id);
	}
	
	$scope.editComment = function(comment) {
		comment.editable = true;
	}

	$scope.saveComment = function(comment) {
		social.saveComment(comment._id.$oid, comment, function(data) {
			comment.editable = false;
		});
	}

	$scope.deleteComment = function(id) {
		social.deleteComment(id);
	}

	$scope.fb_like = function() {
		social.like($scope.id);
	} 
	$scope.getPost();
}])