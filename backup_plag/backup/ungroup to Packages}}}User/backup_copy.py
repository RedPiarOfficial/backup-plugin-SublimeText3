import sublime
import sublime_plugin
import os
import uuid
import configparser
class SaveEventListener(sublime_plugin.EventListener):
	def on_pre_save(self, view):
		self.save_file(view)
		config = configparser.ConfigParser()
		file_path = view.file_name()
		short_extension = os.path.splitext(file_path)[1]
		work_folder = os.path.dirname(sublime.executable_path())
		create_path = f'{work_folder}/backup/{os.path.basename(file_path)}.temp'
		backup_folder = os.path.join(work_folder, 'backup')
		config.read(f"{backup_folder}/backupSettings.ini")
		if short_extension not in config["backup"]["ignored"]:
			existing_files = os.listdir(backup_folder)

			with open(file_path, "r", encoding="utf-8") as file:
				if str(os.path.basename(create_path)) not in existing_files:
					new_file = create_path.split(".")
					with open(f"{new_file[0]}_{uuid.uuid4()}.{new_file[1]}.{new_file[2]}", "w+", encoding="utf-8") as save:
						for line in file.readlines():
							save.write(line)
						if eval(config["backup"]["notification"]):
							sublime.message_dialog(f'backup file save is path:\n{new_file[0]}_{uuid.uuid4()}.{new_file[1]}.{new_file[2]}')


	def save_file(self, view):
		file_path = view.file_name()

		if file_path:
			content = view.substr(sublime.Region(0, view.size()))
			with open(file_path, 'w', encoding='utf-8') as file:
				file.write(content)
