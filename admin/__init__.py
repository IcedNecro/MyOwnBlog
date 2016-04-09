import os, configs

def save_fs(_file, name, id, **kwargs):
	save_dir = os.path.join(configs.settings.UPLOAD_DIRECTORY, str(id))
	
	if os.path.exists(save_dir) == False:
		os.makedirs(save_dir)

	_file.save(os.path.join(save_dir, name))

def remove_fs(filename, id):
	save_dir = os.path.join(configs.settings.UPLOAD_DIRECTORY, str(id))
	os.remove(os.path.join(save_dir, filename))

def get_num_of_files(id):
	save_dir = os.path.join(configs.settings.UPLOAD_DIRECTORY, str(id))
	return len(os.listdir(save_dir))

def list_images(id):
	save_dir = os.path.join(configs.settings.UPLOAD_DIRECTORY, str(id))
	return filter( lambda x: x != 'banner', os.listdir(save_dir))