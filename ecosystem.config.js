module.exports = {
  apps : [{
    name   : "zipit",
    script : "./env/bin/python",
    args   : "./start_gunicorn.sh",
  }]
}