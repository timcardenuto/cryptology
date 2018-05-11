Lattices are hard. As someone who doesn't consider mathematics his primary interest I take solace in the words of whoever wrote the [NTL LLL documentation](http://shoup.net/ntl/doc/LLL.cpp.html):

>I think it is safe to say that nobody really understands how the LLL algorithm works.  The theoretical analyses are a long way from describing what "really" happens in practice.  Choosing the best variant for a certain application ultimately is a matter of trial and error.

## Using liblll
The following is how you use the `liblll` Python library (really a single file) functions:

    for cipherdecimal in ciphertext:
		  M = create_matrix_from_knapsack(publickey,cipherdecimal)
		  M_reduced = lll_reduction(M)
		  plainbits = best_vect_knapsack(M_reduced)
		  plainbits_array.append(plainbits[:10])

    plaintext = decode(plainbits_array)
    print "Plaintext: " + str(plaintext) + "\n"

This includes the helper functions `create_matrix_from_knapsack` and `best_vect_knapsack` which just organize some input and output data for the real heavy lifter `lll_reduction`. The function `decode` in this case is mine, and just maps the plaintext decimal values back to ASCII digraph pairs.

My use/implementation of the liblll functions are wrapped in `lll_lattice_basis_reduction_attack.py` while the Merkle-Hellman knapsack is in it's own file `merkle_hellman_knapsack.py` This keeps things nice and atomic while still allowing you to test both simultaneously as shown next.


### Using merkle_hellman_knapsack.py
From a terminal (Linux) you can pipe plaintext in from a file to get ciphertext out. Plaintext must be all lowercase without punctuation, spaces and newlines will be automatically removed. The private key parameters A, M, W, and therefore public key B all use a default hardcoded value. If you want to edit them you can edit the parameters in the python file (in the main function at the bottom). Or if you're just using the functions directly from another python program, you specify those parameters. If you don't have a text file, there is a default plaintext string 'goddoesnotplaydice'.

Example terminal use:

	$ cat plaintext.txt
	the most merciful thing in the world i think is the inability of the human mind
	to correlate all its contents we live on a placid island of ignorance in the midst
	of black seas of infinity and it was not meant that we should voyage far
	the sciences each straining in its own direction have hitherto harmed us little
	but some day the piecing together of dissociated knowledge will open up such
	terrifying vistas of reality and of our frightful position therein that we shall
	either go mad from the revelation or flee from the light into the peace and safety
	of a new dark age

	$ cat plaintext.txt | python merkle_hellman_knapsack.py
	[8960, 2304, 7592, 9799, 4839, 2192, 4652, 4940, 6233, 5346, 7166, 8960, 5041, 7656, 4595, 7366, 6233, 5612, 5734, 8960, 2038, 5745, 1980, 4797, 2313, 6221, 8960, 6328, 1090, 3067, 3832, 6075, 8497, 2849, 10674, 5238, 3545, 2862, 5764, 7366, 8484, 7390, 8630, 6142, 9454, 5238, 6064, 3872, 5745, 7001, 1568, 7299, 5734, 5899, 6075, 6221, 5933, 4244, 8518, 4443, 2038, 6142, 5967, 3832, 1693, 8497, 5673, 5899, 3760, 7819, 1913, 6221, 7166, 5210, 6914, 2313, 3067, 3460, 745, 1913, 4244, 9799, 2862, 6142, 8960, 3545, 1760, 11019, 5024, 4595, 1236, 2517, 2885, 4041, 9372, 5967, 8484, 4365, 4443, 4775, 2862, 5126, 10183, 8518, 7166, 7166, 3151, 6914, 479, 6592, 6075, 5798, 4430, 8896, 7390, 5064, 2725, 6233, 8960, 4839, 8497, 5064, 8139, 6062, 3561, 4797, 2111, 4531, 3415, 479, 5758, 6062, 1514, 8960, 5504, 4365, 2192, 5346, 8497, 2885, 8960, 4839, 6221, 3460, 8551, 7247, 4099, 8630, 2795, 4244, 5226, 6062, 2885, 2026, 5764, 8958, 3936, 4290, 7886, 5126, 8630, 10674, 5997, 3686, 5346, 3628, 10183, 1913, 6221, 8784, 4369, 7366, 2517, 6075, 6221, 5024, 10416, 7873, 6085, 10262, 4024, 5635, 8085, 8896, 7390, 8960, 4839, 2038, 6142, 5064, 745, 4775, 5064, 5764, 2038, 8960, 4839, 5622, 4477, 4826, 7474, 8201, 5967, 8784, 2725, 5899, 8896, 7390, 7656, 5540, 3128, 6018, 5758, 8960, 5238, 5933, 6555, 7166, 8497, 8960, 5504, 2862, 1926, 3067, 1693, 1898, 6407, 5520, 4041, 6011, 5871, 1977, 2817, 2885]


You can also pipe the ciphertext output of `merkle_hellman_knapsack.py` to the `lll_lattice_basis_reduction_attack.py` file to run it through the LLL algorithm attack.

	$ cat plaintext.txt | python merkle_hellman_knapsack.py | python lll_lattice_basis_reduction_attack.py
	### Recovered plaintext:
	------tmercifu----ngin----orldit----is----nability----ehumanmindtocorr--ateallitscon--ntsw--iv--naplacidis--n 		
	d--ignoranc--nthemidstofb----seas--infinityan--twasnotmeant--atweshould----gefarthescienceseachstraininginits
	owndirec--on--ve----erto--rmeduslittlebutsomeday----iecingtoge--er----ss--ia--dknowledgewillop--upsuch--rrify
	ingvistas----alit--nd--ourfrigh--ulposi--on--er--nt--twes--ll----ergomadfromthe--ve----onorfleefrom----ightin
	to----eaceandsafet--fa----arkage

Clearly there are a few errors here, though it did a decent job, enough that standard cryptanalysis could figure out the rest. The two errors resulted in`aa` digraphs which is basically the value `00`. Each time this happens the `liblll` library prints the following to stdout:

    No direct solution found, apply heuristic
    no solution found with heuristics

Not sure what's going on here, other versions of the algorithm have similar results. There are several libraries with LLL support:

#### Python
* [liblll](https://github.com/kutio/liblll) - the easiest to get working, simply clone source and use in your project folder. Pip install didn't work. Blog here was helpful (http://kutioo.blogspot.com/2011/12/liblll.html)
* [fpylll](https://github.com/fplll/fpylll) - *should* have worked easily but couldn't get it installed with all the dependencies on CentOS 7. It's a python frontend for the C library fplll and relies on cython which had problems installing due to cysignals which has to be compiled without FORTIFY_SOURCE. Nearest I can tell this is something that's a problem on CentOS due to security measures like SELinux... not worth mucking with.
* [pymatgen](http://pymatgen.org/) - this is listed on Wikipedia, but be aware it only supports 3x3 matrices... so seems useless for crypto problems.

#### C/C++
* [fplll](https://github.com/fplll/fplll) - Floating Point LLL (FPLLL) is one of the more prominent in Google searches and was simple to clone and build from source. Getting a basic client program example working with it isn't as straight forward as liblll however...
* [ntl](http://shoup.net/ntl) - Number Theory Library (NTL) is listed on Wikipedia, wasn't too hard to download, build, and hack an example to use.

#### Other Info
* https://kel.bz/post/lll/ - helpful blog about the LLL algorithm in general, with code snippets
* http://www.math.ucsd.edu/~crypto/Projects/JenniferBakker/Math187/#Anchor-Attackin-35484 - blog about the LLL algorithm, not sure it's input/output is actually correct... but gives 1 data point.
* http://kutioo.blogspot.com/2011/12/liblll.html - blog about using liblll
* https://martinralbrecht.wordpress.com/2016/04/03/fpylll/ - blog about using fpylll
*
