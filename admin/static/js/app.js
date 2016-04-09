var adminApp = angular.module('adminApp',['ngFileUpload']);


adminApp.controller('adminIndex', ['$scope', '$http', function ($scope, $http) {
	
	$scope.getAvailablePosts = function(fiter_data) {
		console.log(fiter_data)
		$http({
			method: 'GET', 
			url: '/admin/api/post',
			params: fiter_data
		}).success(function(data) {
			$scope.posts = data.data 
		})
	}
	$scope.setDisplayMode = function (mode) {
		filter = {}
		if(mode=='in_process') {
			filter['not_published']=true
		}
		$scope.getAvailablePosts(filter)
	}

	$scope.deletePosts = function() { 
		var args = []
		for(var i in $scope.posts) {
			if($scope.posts[i].selected==true)
				args.push($scope.posts[i]._id)
		}
		$http({
			method: 'DELETE', 
			url: '/admin/api/post',
			params: {'ids':args+''}
		}).success(function(data) {
			$scope.posts = data.data 
		})	
	}
	$scope.uploadPhoto = function() {
		
	}
	$scope.getAvailablePosts();
}])

adminApp.controller('postCRUDController',['$scope', '$http', 'Upload', function($scope, $http, Upload){
	var md = new showdown.Converter()
	md.setOption('tables', true)
	$scope.images = []
	$scope.selected = [];
	$scope.newPost = {};
	$scope.tagName = '';

	getTags = function(initial) {
		$http({
			method: 'GET',
			url: '/admin/api/tags',
			params: initial ? {} : {text:$scope.tagName}
		}).success(function(data) {
			if(data.data.tags.length == 0) {
				$scope.notSelected = [$scope.tagName];
			} else {
				$scope.notSelected = data.data.tags.slice(0,5);
			}
		}).error(function() {
			$scope.notSelected = ["Hello",'Bye','Heil']
		})
	}

	$scope.getTags = getTags;
	$scope.refreshMarkdown = function (text) {
		$('.preview>*').remove()
		$('.preview').append(md.makeHtml(text))
	}

	$scope.addToSelected = function(tag) {
		var i = $scope.notSelected.indexOf(tag);
		$scope.notSelected.splice(i,1);
		$scope.newPost.tags.push(tag);
	}

	$scope.removeFromSelected = function(tag) {
		var i = $scope.newPost.tags.indexOf(tag);
		$scope.newPost.tags.splice(i,1);
		$scope.notSelected.push(tag);
	}	
	$scope.append_to_selected_images = function(file) {
		$scope.upload(file, {}, function(file) {
			$scope.images.push(file.name);
		});
	}

	$scope.delete_image = function(file) {
		var id = $('body').attr('post')
		
		$scope.images.splice($scope.images.indexOf(file), 1)
		$http({
			url: '/admin/api/post/image/'+id,
			method:'DELETE',
			params: {src: file}
		}).success(function(data) {
			console.log('file deleted')
		})
	}

    $scope.upload = function (file, opts, calback) {
		var id = $('body').attr('post')

        Upload.upload({
            url: '/admin/api/post/image/'+id,
        	params: opts,
            data: {file: file,}
        }).then(function (resp) {
            console.log('Success ' + resp.config.data.file.name + 'uploaded. Response: ' + resp.data);
            if(calback) {
            	calback(file)
            }
        });
    };

    getTags(true)
}])

adminApp.controller('postController',['$scope', '$http', '$controller', function ($scope, $http, $controller) {
	angular.extend(this, $controller('postCRUDController', {$scope: $scope}))

	$scope.sendData = function() {
		$scope.newPost.tags = $scope.selected.slice();
		$http({
			'method': 'POST', 
			'data': $scope.newPost,
			'url': '/admin/api/post'
		}).success(function() {
			
		})
	}

	$scope.getTags();
}]);

adminApp.controller('postEditController',['$scope', '$http', '$controller', function ($scope, $http, $controller) {
	angular.extend(this, $controller('postCRUDController', {$scope: $scope}))
	var firstState = true;

	$scope.getData = function() {
		var id = $('body').attr('post')
		$scope.newPost.tags = $scope.selected.slice();
		$http({
			method: 'GET', 
			url: '/admin/api/post/'+id,
		}).success(function(data) {
			if(firstState) {
				$scope.initial = jQuery.extend(true, {}, data.data);
				firstState = false;
			}
			$scope.newPost = data.data;	
		})
	}
	
	$scope.publishPost = function(b) {
		$scope.newPost.published = b;
		$scope.updateData();
	}

	$scope.updateData = function() {
		var changes = {}

		var id = $('body').attr('post')
		for(var i in $scope.newPost) {
			if($scope.newPost[i] != $scope.initial[i])
				changes[i] = $scope.newPost[i]
		}

		delete changes.images 
		$http({
			method:'PUT', 
			url: '/admin/api/post/'+id,
			data: changes
		}).success(function(data) {
			$scope.getData();
		})
	}

	$scope.getData(true);
}]);