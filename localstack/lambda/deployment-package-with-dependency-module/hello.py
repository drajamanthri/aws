def handler(event, context):
    import hello_layer
    hello_layer.util()

    print('hello')
    return 'hello'