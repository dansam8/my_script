import my_scrypt

#print(my_scrypt.__doc__)
#print(runn.help())

runn = my_scrypt.runner()
runn.set_path('test_script.txt')
runn.booltesting = False

runn.run_code()
