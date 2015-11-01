/*
 *
 * Author: Jeffrey Leung
 * Last edited: 2015-11-01
 *
 * This C++ header file contains functions which can be used to print
 * the contents of an array or vector.
 *
 */

#ifndef PRINT_DATA_STRUCTURES_HPP_
#define PRINT_DATA_STRUCTURES_HPP_

#include <iostream>
#include <iterator>
#include <vector>

// Function prototypes:

// This function prints the contents of a given array in a horizontal list,
// surrounded by square brackets [].
template <class T>
void PrintArrayHorizontal( T* arr, unsigned int len );

// This function prints the contents of a given vector in a horizontal list,
// surrounded by square brackets [].
template <class T>
void PrintVectorHorizontal( std::vector<T> v );

// This function prints the contents of a given vector in a vertical list.
template <class T>
void PrintVectorVertical( std::vector<T> v );


// Function implementations:

// This function prints the contents of a given array in a horizontal list,
// surrounded by square brackets [].
template <class T>
void PrintArrayHorizontal( T* arr, unsigned int len )
{
  std::cout << "[ ";
  for( unsigned int i = 0; i < len; ++i )
  {
    std::cout << arr[i] << " ";
  }
  std::cout << "]";
  
  return;
}

// This function prints the contents of a given vector in a horizontal list,
// surrounded by square brackets [].
template <class T>
void PrintVectorHorizontal( std::vector<T> v )
{
  std::cout << "[ ";
  
  for( typename std::vector<T>::iterator v_index = v.begin();
       v_index != v.end();
       std::advance( v_index, 1 ) )
  {
    std::cout << *v_index
              << " ";
  }
  
  std::cout << "]";

  return;
}

// This function prints the contents of a given vector in a vertical list.
template <class T>
void PrintVectorVertical( std::vector<T> v )
{
  for( typename std::vector<T>::iterator v_index = v.begin();
       v_index != v.end();
       std::advance( v_index, 1 ) )
  {
    std::cout << *v_index
              << std::endl;
  }
  
  return;
}

#endif  // PRINT_DATA_STRUCTURES_HPP_
