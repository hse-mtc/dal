import { MessageBox } from 'element-ui'

export function getCoords(elem) {
  let box = elem.getBoundingClientRect();

  return {
    top: box.top + window.pageYOffset,
    left: box.left + window.pageXOffset
  };
}

export function handleClose(done) {
  MessageBox.confirm('Уверены?')
    .then(_ => {
      done()
    })
    .catch(_ => {
    })
}
