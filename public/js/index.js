const button = document.querySelector("button")
const input = document.querySelector("input")
let tasks

const addTask = async () => {
    const { value } = input
    
    const details = await fetch("/add-task", {
        method: "POST",
        headers: {
            "content-type": "application/json"
        },
        body: JSON.stringify({
            content: value
        })
    }).then(res => res.text())

    renderTask(value)
    input.value = ""
}

const taskInteraction = () => {
    updateTasks()

    for(const task of tasks) {
        const span = task.querySelector("span")
        const [ trash, check ] = task.querySelectorAll('i')
        
        span.style.textDecoration = task.dataset.status == "True" ? "line-through" : "none"
        
        trash.onclick = () => {
            fetch(`/delete/${ task.dataset.id }`)
            task.remove()
        }
        
        check.onclick = () => {
            fetch(`/complete/${ task.dataset.id }`)
            task.dataset.status = task.dataset.status == "True" ? "False" : "True"
            span.style.textDecoration = task.dataset.status == "True" ? "line-through" : "none"
        }
    }
}

const renderTask = (value) => {
    updateTasks()

    const taskWrapper = document.getElementsByClassName("task-wrapper")[0]
    taskWrapper.innerHTML += 
    `
    <div class="task" data-status="False" data-id="${ tasks.length }">
        <span>${ value }</span>
        <div class="task-options">
            <i class="far fa-trash-alt"></i>
            <i class="far fa-calendar-check"></i>
        </div>
    </div>
    `

    taskInteraction()
}

const updateTasks = () => {
    tasks = document.getElementsByClassName("task")
}

button.addEventListener("click", addTask)
input.addEventListener("keydown", e => {
    if(e.key == "Enter") {
        addTask()
    }
})
taskInteraction()