/*
 *  test2Priv.h
 *  test2
 *
 *  Created by Tony Castronova on 11/11/14.
 *  Copyright (c) 2014 Tony Castronova. All rights reserved.
 *
 */

/* The classes below are not exported */
#pragma GCC visibility push(hidden)

class test2Priv
{
	public:
		void HelloWorldPriv(const char * value);
};

#pragma GCC visibility pop
