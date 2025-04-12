function searchCommands() {
    let query = document.getElementById("command-search").value.toLowerCase();
    let commands = document.querySelectorAll(".commands tr:not(:first-child)");
    let anyMatch = false;
    commands.forEach(command => {
        let commandName = command.children[0].textContent.toLowerCase();
        let commandType = command.children[1].textContent.toLowerCase();
        let commandDescription = command.children[2].textContent.toLowerCase();
        let match = false;
        if (commandName.includes(query) || commandType.includes(query) || commandDescription.includes(query)) {
            match = true;
        }
        if (commandName.endsWith('*') && query.startsWith(commandName.slice(0, -1))) {
            match = true;
        }
        if (match) {
            anyMatch = true;
            command.classList.remove('hidden');
        } else {
            command.classList.add('hidden');
        }
    });
    // if no matches, display all
    if (!anyMatch) {
        commands.forEach(command => command.classList.remove('hidden'));
    }
}

window.addEventListener('load', () => {
    searchCommands();
});
